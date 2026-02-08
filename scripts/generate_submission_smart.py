import pandas as pd
import numpy as np

# Загружаем кандидатов и цели
candidates = pd.read_csv("data/submit/candidates.csv")  # columns: user_id, edition_id, genre
targets = pd.read_csv("data/submit/targets.csv")        # columns: user_id

MAX_TOP = 20
BASE_GENRE_LIMIT = 3  # базовое ограничение на один жанр

submission_rows = []

for user, group in candidates.groupby('user_id'):
    group = group.sample(frac=1, random_state=42)  # случайный порядок, можно заменить на score если есть
    selected = []
    genre_count = {}
    
    for _, row in group.iterrows():
        genre = row.get('genre', 'unknown')
        # динамическое ограничение жанра
        limit = BASE_GENRE_LIMIT + (MAX_TOP - len(selected)) // 5
        if genre_count.get(genre, 0) >= limit:
            continue
        selected.append(row['edition_id'])
        genre_count[genre] = genre_count.get(genre, 0) + 1
        if len(selected) == MAX_TOP:
            break

    # если не набралось 20, дополняем оставшимися книгами
    if len(selected) < MAX_TOP:
        for eid in group['edition_id']:
            if eid not in selected:
                selected.append(eid)
            if len(selected) == MAX_TOP:
                break

    for rank, eid in enumerate(selected, 1):
        submission_rows.append({'user_id': user, 'edition_id': eid, 'rank': rank})

submission = pd.DataFrame(submission_rows)

# Сохраняем сабмит
submission.to_csv("submission.csv", index=False)

# Проверка
assert submission.groupby('user_id')['edition_id'].count().eq(MAX_TOP).all(), "Ошибка: не 20 рекомендаций на пользователя"
assert submission.duplicated(subset=['user_id','edition_id']).sum() == 0, "Ошибка: дублируются edition_id"
print("✅ Сабмит готов и проверен!")
