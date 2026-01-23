"""
Скрипт для работы с пользователями через Django shell
Использование:
1. Запустите: python manage.py shell
2. Скопируйте и выполните команды ниже
"""

# Импорт модели User
from users.models import User

# Показать всех пользователей
print("=== Список всех пользователей ===")
users = User.objects.all()
for i, user in enumerate(users, 1):
    print(f"{i}. ID: {user.id} | Email: {user.email} | Активен: {user.is_active} | Дата регистрации: {user.date_joined}")

# Выбрать пользователя по ID (замените 1 на нужный ID)
user_id = 1  # Измените на нужный ID
user_to_delete = User.objects.get(id=user_id)
print(f"\nВыбран пользователь: {user_to_delete.email}")

# Показать информацию о пользователе перед удалением
print(f"Email: {user_to_delete.email}")
print(f"Активен: {user_to_delete.is_active}")
print(f"Дата регистрации: {user_to_delete.date_joined}")

# Удалить пользователя (раскомментируйте для удаления)
# user_to_delete.delete()
# print(f"Пользователь {user_to_delete.email} удален!")

# Альтернативный способ: удалить по email
# email_to_delete = "example@mail.com"  # Замените на нужный email
# user_to_delete = User.objects.get(email=email_to_delete)
# user_to_delete.delete()
# print(f"Пользователь {email_to_delete} удален!")
