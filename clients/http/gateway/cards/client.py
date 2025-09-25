from httpx import Response
from clients.http.client import HTTPClient
from typing import TypedDict


class IssueCardRequestDict(TypedDict):
    """
    Структура данных для выпуска виртуальной или физической карты
    """
    userId: str
    accountId: str

class CardsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/cards сервиса http-gateway.
    """
    def issue_virtual_card_api(self, request: IssueCardRequestDict) -> Response:
        """
         Создание виртуальной карты.
         :param request: Словарь с данными пользователя для создания карты.
         :return: Ответ от сервера (объект httpx.Response).
         """
        return self.post("/api/v1/cards", json=request)

    def issue_physical_card_api(self, request: IssueCardRequestDict) -> Response:
        """
         Создание физической карты.
         :param request: Словарь с данными пользователя для создания карты.
         :return: Ответ от сервера (объект httpx.Response).
         """
        return self.post("/api/v1/cards", json=request)
