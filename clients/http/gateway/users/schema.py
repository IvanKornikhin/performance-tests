from pydantic import BaseModel, Field, EmailStr, ConfigDict

from tools.fakers import fake


# Добавили суффикс Schema вместо Dict
class UserSchema(BaseModel):  # Наследуем от BaseModel вместо TypedDict
    """
    Описание структуры пользователя.
    """
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")  # Использовали alise
    first_name: str = Field(alias="firstName")  # Использовали alise
    middle_name: str = Field(alias="middleName")  # Использовали alise
    phone_number: str = Field(alias="phoneNumber")  # Использовали alise


# Добавили суффикс Schema вместо Dict
class GetUserResponseSchema(BaseModel):  # Наследуем от BaseModel вместо TypedDict
    """
    Описание структуры ответа получения пользователя.
    """
    user: UserSchema


# Добавили суффикс Schema вместо Dict
class CreateUserRequestSchema(BaseModel):
    """
    Структура данных для создания нового пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    # Добавили генерацию случайного email
    email: EmailStr = Field(default_factory=fake.email)
    # Добавили генерацию случайной фамилии
    last_name: str = Field(alias="lastName", default_factory=fake.last_name)
    # Добавили генерацию случайного имени
    first_name: str = Field(alias="firstName", default_factory=fake.first_name)
    # Добавили генерацию случайного отчества
    middle_name: str = Field(alias="middleName", default_factory=fake.middle_name)
    # Добавили генерацию случайного номер телефона
    phone_number: str = Field(alias="phoneNumber", default_factory=fake.phone_number)


# Добавили суффикс Schema вместо Dict
class CreateUserResponseSchema(BaseModel):  # Наследуем от BaseModel вместо TypedDict
    """
    Описание структуры ответа создания пользователя.
    """
    user: UserSchema
