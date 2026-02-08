import pandas as pd

# Загрузка данных
candidates = pd.read_csv("data/submit/candidates.csv")  # user_id, edition_id, genre
interactions = pd.read_csv("data/data_user_interactions.csv")  # user_id, edition_id, interaction_weight
targets = pd.read_csv("data/submit/targets.csv")  # user_id для сабмита

# Расчет персонализированного скора
candidates_profile = candidates.merge(interactions, on=['user_id','edition_id'], how='left').fillna(0)
candidates_profile['score'] = candidates_profile['interaction_weight']

# Настройка динамического ограничения по жанру
MAX_TOP = 20
BASE_GENRE_LIMIT = 3  # базовое ограничение на один жанр
submission_rows = []

for user, group in candidates_profile.groupby('user_id'):
    group = group.sort_values('score', ascending=False)
    selected = []
    genre_count = {}
    
    for _, row in group.iterrows():
        genre = row.get('genre', 'unknown')
        # Динамическое уменьшение приоритета жанра, если его слишком много в топе
        limit = BASE_GENRE_LIMIT + (MAX_TOP - len(selected)) // 5
        if genre_count.get(genre, 0) >= limit:
            continue
        selected.append(row['edition_id'])
        genre_count[genre] = genre_count.get(genre, 0) + 1
        if len(selected) == MAX_TOP:
            break

    # Если топ-20 не набрался, дополняем оставшимися лучшими книгами
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

# Проверки
assert submission.groupby('user_id')['edition_id'].count().eq(20).all(), "Ошибка: не 20 рекомендаций на пользователя"
assert submission.duplicated(subset=['user_id','edition_id']).sum() == 0, "Ошибка: дублируются edition_id"
print("✅ Сабмит готов и проверен!")
