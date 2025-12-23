from pydantic import BaseModel
# BaseModel — это базовый класс Pydantic, от которого мы наследуем нашу модел

class User(BaseModel):
    id: int
    name: str
    email: str
# При создании объекта User Pydantic автоматически проверяет, что id — это число, а name и email — строки.

user = User(id=1, name="Alice", email="alice@example.com")
print(user)