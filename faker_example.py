from faker import Faker
import requests

fake = Faker()

# Генерация фейковых данных
user_data = {
    "name": fake.name(),
    "email": fake.email(),
    "age": fake.random_int(min=18, max=100)
}

# Отправка POST-запроса с фейковыми данными
response = requests.post("https://api.example.com/users", json=user_data)

# Проверка, что запрос прошел успешно
assert response.status_code == 201
