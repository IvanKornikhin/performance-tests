from pydantic import BaseModel, EmailStr, constr


class UserSchema(BaseModel):
    """класс для создания пользователя"""
    id: str
    email: EmailStr
    last_name: str
    first_name: constr(min_length=2, max_length=50)
    middle_name: str
    phone_number: str


class CreateUserRequestSchema(BaseModel):
    """класс для запроса создания пользователя"""
    email: EmailStr
    last_name: str
    first_name: constr(min_length=2, max_length=50)
    middle_name: str
    phone_number: str


class CreateUserResponseSchema(BaseModel):
    """класс для ответа на запрос создания пользователя"""
    user: UserSchema
