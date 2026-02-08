import pandas as pd

fixed = pd.read_csv("submission_FINAL.csv")

# Количество пользователей и строк
print("Пользователей:", fixed['user_id'].nunique())
print("Строк:", len(fixed))

# Проверки
assert fixed.groupby('user_id').size().eq(20).all(), "❌ У кого-то не 20 книг"
assert fixed.duplicated(subset=['user_id','edition_id']).sum() == 0, "❌ Есть дубликаты"
print("✅ Проверки пройдены")
