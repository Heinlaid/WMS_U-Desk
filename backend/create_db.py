from app import app, db

# Создание контекста приложения
with app.app_context():
    print("Создаём таблицы в базе данных...")
    db.create_all()
    print("Готово! Все таблицы созданы.")
