import pandas as pd

# 1. Загружаем файлы
example = pd.read_csv("data/example_submission.csv")
sub = pd.read_csv("data/submission_smart.csv")

# 2. Разрешённые книги
allowed_editions = set(example['edition_id'].unique())

# Оставляем только разрешённые edition_id
sub = sub[sub['edition_id'].isin(allowed_editions)]

# Убираем дубликаты
sub = sub.drop_duplicates(subset=["user_id", "edition_id"])

# 3. Функция исправления одного пользователя
def fix_user(group, user):
    current = set(group['edition_id'])
    missing = list(allowed_editions - current)
    needed = 20 - len(current)

    if needed > 0:
        add = missing[:needed]
        df_add = pd.DataFrame({
            'user_id': [user]*needed,
            'edition_id': add,
            'rank': [0]*needed
        })
        group = pd.concat([group, df_add], ignore_index=True)

    group = group.head(20)
    group = group.sort_values('edition_id').reset_index(drop=True)
    group['rank'] = range(1, 21)

    return group

# 4. Применяем ко всем пользователям
fixed_list = []

for user in example['user_id'].unique():
    user_group = sub[sub['user_id'] == user]
    fixed_user = fix_user(user_group, user)
    fixed_list.append(fixed_user)

fixed = pd.concat(fixed_list, ignore_index=True)

# 5. Проверки
assert fixed.groupby('user_id').size().eq(20).all()
assert fixed.duplicated(subset=['user_id','edition_id']).sum() == 0
assert set(fixed['edition_id']) <= allowed_editions

# 6. Сохраняем финальный сабмит
fixed.to_csv("submission_FINAL.csv", index=False, encoding="utf-8", lineterminator="\n")
print("🔥 Файл submission_FINAL.csv готов")
