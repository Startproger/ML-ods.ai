import pandas as pd

# Загружаем данные
candidates = pd.read_csv("data/submit/candidates.csv")
interactions = pd.read_csv("data/data_user_interactions.csv")  # таблица с историей пользователя
targets = pd.read_csv("data/submit/targets.csv")  # список пользователей для сабмита

# Считаем скор (пример: сумма взаимодействий по пользователю и книге)
candidates_profile = candidates.merge(interactions, on=['user_id', 'edition_id'], how='left').fillna(0)
candidates_profile['score'] = candidates_profile['interaction_weight']

# Подготовка сабмита
submission_rows = []

MAX_PER_GENRE = 3  # ограничение книг одного жанра в топ-20
for user, group in candidates_profile.groupby('user_id'):
    # сортируем по скору
    group = group.sort_values('score', ascending=False)
    
    selected = []
    genre_count = {}
    
    for _, row in group.iterrows():
        genre = row['genre'] if 'genre' in row else 'unknown'
        
        # проверяем, не превысили лимит жанра
        if genre_count.get(genre, 0) >= MAX_PER_GENRE:
            continue
        
        selected.append(row['edition_id'])
        genre_count[genre] = genre_count.get(genre, 0) + 1
        
        if len(selected) == 20:
            break
    
    # Если топ-20 не набрался, дополняем оставшимися топовыми по скору
    if len(selected) < 20:
        for eid in group['edition_id']:
            if eid not in selected:
                selected.append(eid)
            if len(selected) == 20:
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
