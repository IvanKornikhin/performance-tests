from httpx import Response
from typing import TypedDict
from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client  # Импортируем builder


class DocumentDict(TypedDict):
    """
    Описание структуры документа.
    """
    url: str
    document: str


class GetTariffDocumentResponseDict(TypedDict):
    """
    описание структуры ответа создания документа по тарифу
    """
    tariff: DocumentDict


class GetContractDocumentResponseDict(TypedDict):
    """
    описание структуры ответа создания документа по контракту
    """
    contract: DocumentDict


class DocumentsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/documents сервиса http-gateway.
    """

    def get_tariff_document_api(self, account_id: str) -> Response:
        """
        Получить тарифа по счету.

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"/api/v1/documents/tariff-document/{account_id}")

    def get_contract_document_api(self, account_id: str) -> Response:
        """
        Получить контракта по счету.

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"/api/v1/documents/contract-document/{account_id}")

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseDict:
        """получение ответа создания тарифного документа"""
        response = self.get_tariff_document_api(account_id)
        return response.json()

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseDict:
        """получение ответа создания контрактного документа"""
        response = self.get_contract_document_api(account_id)
        return response.json()


# Добавляем builder для DocumentsGatewayHTTPClient
def build_documents_gateway_http_client() -> DocumentsGatewayHTTPClient:
    """
    Функция создаёт экземпляр DocumentsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию DocumentsGatewayHTTPClient.
    """
    return DocumentsGatewayHTTPClient(client=build_gateway_http_client())

