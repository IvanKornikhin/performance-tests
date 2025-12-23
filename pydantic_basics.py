# Итоги
# В этом уроке мы подробно разобрали основные возможности Pydantic и научились работать с валидацией данных. Вот основные моменты, которые мы рассмотрели:
#
# Основные принципы Pydantic
#
# Использование BaseModel для создания схем данных.
# Валидация входных данных на основе аннотаций типов.
# Преобразование типов и автоматическая нормализация данных.
# Field и alias
#
# Как использовать Field для задания alias (альтернативных названий полей).
# Возможность указания значений по умолчанию и использования default_factory.
# Вложенные модели
#
# Использование одной Pydantic-модели внутри другой (пример с CardSchema в AccountSchema).
# Валидация встроенных типов
#
# Использование EmailStr, HttpUrl и других встроенных типов для автоматической проверки значений.
# Пример с DocumentSchema, где HttpUrl не позволяет передавать некорректные URL.
# Способы инициализации моделей
#
# Передача аргументов в конструктор.
# Использование словаря (dict).
# Разбор JSON (model_validate_json).
# Обработка ошибок валидации
#
# Как Pydantic сообщает об ошибках.
# Использование ValidationError и error.errors() для детального разбора ошибок.
# Теперь у вас есть отличная база для работы с Pydantic в более сложных сценариях, включая API-клиенты, обработку данных из JSON, интеграцию с базами данных и другие задачи.

import uuid
from datetime import date

from pydantic import BaseModel, Field, HttpUrl, EmailStr, ValidationError


# Добавили модель DocumentSchema
class DocumentSchema(BaseModel):
    url: HttpUrl  # Используем HttpUrl вместо str
    document: str


# Добавили модель UserSchema
class UserSchema(BaseModel):
    id: str
    email: EmailStr  # Используем EmailStr вместо str
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    phone_number: str = Field(alias="phoneNumber")


# Добавили модель CardSchema
class CardSchema(BaseModel):
    id: str = "card-id"
    pin: str = "1234"
    cvv: str = "123"
    type: str = "PHYSICAL"
    status: str = "ACTIVE"
    account_id: str = Field(alias="accountId", default="account-id")
    card_number: str = Field(alias="cardNumber", default="123412341234234")
    card_holder: str = Field(alias="cardHolder", default="Alise Smith")
    expiry_date: date = Field(alias="expiryDate", default=date(2027, 3, 25))
    payment_system: str = Field(alias="paymentSystem", default="VISA")


class AccountSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str = "CREDIT_CARD"
    # Вложенный объект для списка карт привязанных к счету
    cards: list[CardSchema] = Field(default_factory=list)
    status: str = "ACTIVE"
    balance: float = 25000

    def get_account_name(self) -> str:
        return f"{self.status}:{self.type}"


# Инициализируем модель AccountSchema через передачу аргументов
account_default_model = AccountSchema(
    id="account-id",
    type="CREDIT_CARD",
    # Добавили инициализацию списка вложенных моделей CardSchema
    cards=[
        CardSchema(
            id="card-id",
            pin="1234",
            cvv="123",
            type="PHYSICAL",
            status="ACTIVE",
            accountId="account-id",
            cardNumber="1234123412341234",
            cardHolder="Alise Smith",
            expiryDate=date(2027, 3, 25),
            paymentSystem="VISA"
        )
    ],
    status="ACTIVE",
    balance=100.57,
)
print('Account default model:', account_default_model)

# Инициализируем модель AccountSchema через распаковку словаря
account_dict = {
    "id": "account-id",
    "type": "CREDIT_CARD",
    # Добавили ключ cards
    "cards": [
        {
            "id": "card-id",
            "pin": "1234",
            "cvv": "123",
            "type": "PHYSICAL",
            "status": "ACTIVE",
            "accountId": "account-id",
            "cardNumber": "1234123412341234",
            "cardHolder": "Alise Smith",
            "expiryDate": "2027-03-25",
            "paymentSystem": "VISA"
        }
    ],
    "status": "ACTIVE",
    "balance": 777.11,
}
account_dict_model = AccountSchema(**account_dict)
print('Account dict model:', account_dict_model)

# Инициализируем модель AccountSchema через JSON
account_json = """
{
    "id": "account-id",
    "type": "CREDIT_CARD",
    "cards": [
        {
            "id": "card-id",
            "pin": "1234",
            "cvv": "123",
            "type": "PHYSICAL",
            "status": "ACTIVE",
            "accountId": "account-id",
            "cardNumber": "1234123412341234",
            "cardHolder": "Alise Smith",
            "expiryDate": "2027-03-25",
            "paymentSystem": "VISA"
        }
    ],
    "status": "ACTIVE",
    "balance": 777.11
}
"""
account_json_model = AccountSchema.model_validate_json(account_json)
print('Account JSON model:', account_json_model)

try:
    tariff = DocumentSchema(
        url="localhost",
        document="document-data",
    )
except ValidationError as error:
    print(error)
    print(error.errors())
