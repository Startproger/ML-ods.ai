Система рекомендаций книг для пользователей. Для каждого пользователя формируется топ-20 изданий (edition_id) из пула кандидатов на следующий период. Используется TF-IDF и Cosine similarity.

Структура проекта
data/raw/       — исходные данные
data/submit/    — кандидаты и цели
scripts/
    clean_data.py           — подготовка данных и рекомендации
    generate_submission.py  — генерация сабмита
    tests.py                — проверка сабмита
submission.csv  — результат работы
requirements.txt

Установка и запуск
python -m venv venv
& venv/Scripts/Activate.ps1    # Windows PowerShell
pip install -r requirements.txt
python -m scripts.generate_submission
python -m scripts.tests        # проверить сабмит

Формат сабмита

user_id,edition_id,rank

rank от 1 до 20 (1 — верх витрины)

На пользователя ровно 20 строк

Все edition_id из пула кандидатов