from typing import TypedDict
from httpx import Response, QueryParams
from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client


class OperationDict(TypedDict):
    """
    Описание структуры операции
    """
    id: str
    type: str
    status: str
    amount: float
    cardId: str
    category: str
    createdAt: str
    accountId: str


class OperationReceiptDict(TypedDict):
    """Описание структуры чека"""
    url: str
    document: str


class OperationSummaryDict(TypedDict):
    """Описание структуры элемента статистики по операциям"""
    spentAmount: float
    receivedAmount: float
    cashbackAmount: float


class GetOperationsResponseDict(TypedDict):
    """ Описание структуры ответа на запрос списка операций
    """
    operations: list[OperationDict]


class GetOperationsQueryDict(TypedDict):
    """
    Структура данных для получения списка операций.
    """
    accountId: str


class GetOperationsSummaryResponseDict(TypedDict):
    """
    Структура данных для получения статистики по операциям для определенного счета.
    """
    summary: OperationSummaryDict


class GetOperationsSummaryQueryDict(GetOperationsQueryDict):
    """
    Структура данных для получения статистики по операциям для определенного счета.
    """


class GetOperationReceiptResponseDict(TypedDict):
    """
    Структура данных для получения чека по операции.
    """
    receipt: OperationReceiptDict


class GetOperationResponseDict(TypedDict):
    """
    Структура данных для получения информации об операции.
    """
    operation: OperationDict


class MakeOperationRequestDict(TypedDict):
    """
    Базовый класс для создания операций.
    """
    status: str
    amount: float
    cardId: str
    accountId: str


class MakeFeeOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для cоздания операции комиссии.
    """


class MakeFeeOperationResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос создания операции комиссии.
    """
    operation: OperationDict


class MakeTopUpOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для cоздания операции пополнения.
    """


class MakeTopUpOperationResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос создания операции пополнения.
    """
    operation: OperationDict


class MakeCashbackOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для cоздания операции кешбэка.
    """


class MakeCashbackOperationResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос создания операции кешбэка.
    """
    operation: OperationDict


class MakeTransferOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для cоздания операции перевода.
    """


class MakeTransferOperationResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос создания операции перевода.
    """
    operation: OperationDict


class MakePurchaseOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для cоздания операции покупки.
    """
    category: str


class MakePurchaseOperationResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос создания операции покупки.
    """
    operation: OperationDict


class MakeBillPaymentOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для cоздания операции оплаты по счету.
    """


class MakeBillPaymentOperationResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос создания операции оплаты по счету.
    """
    operation: OperationDict


class MakeCashWithdrawalOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для cоздания операции снятия наличных денег.
    """


class MakeCashWithdrawalOperationResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос создания операции снятия наличных денег.
    """
    operation: OperationDict


class OperationsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/operations сервиса http-gateway.
    """

    def get_operations_api(self, query: GetOperationsQueryDict) -> Response:
        """
        Выполняет GET-запрос на получение списка операций.

        :param query: Словарь с параметрами запроса {'accountId': '123'}.
        :return: Объект httpx.Response с данными по списку операций.
        """
        return self.get("/api/v1/operations", params=QueryParams(**query))

    def get_operations(self, account_id: str) -> GetOperationsResponseDict:
        """получение ответа на запрос списка операций """
        query = GetOperationsQueryDict(accountId=account_id)
        response = self.get_operations_api(query)
        return response.json()

    def get_operations_summary_api(self, query: GetOperationsSummaryQueryDict) -> Response:
        """
        Выполняет GET-запрос на получение статистики по операциям для определенного счета.
        :param query: Словарь с параметрами запроса {'accountId': '123'}.
        :return: Объект httpx.Response с данными статистики по операциям для определенного счета.
        """
        return self.get("/api/v1/operations/operations-summary", params=QueryParams(**query))

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponseDict:
        """получение ответа на запрос статистики по операциям для определенного счета"""
        query = GetOperationsSummaryQueryDict(accountId=account_id)
        response = self.get_operations_summary_api(query)
        return response.json()

    def get_operation_receipt_api(self, operation_id: str) -> Response:
        """
        Получение чека по операции по operation_id.
        :param operation_id: Идентификатор операции.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"/api/v1/operations/operation-receipt/{operation_id}")

    def get_operation_receipt(self, operation_id: str) -> GetOperationReceiptResponseDict:
        """ получение ответа на запрос чека по операции"""
        response = self.get_operation_receipt_api(operation_id)
        return response.json()

    def get_operation_api(self, operation_id: str) -> Response:
        """
        Получение информации об операции по operation_id.
        :param operation_id: Идентификатор операции.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"/api/v1/operations/{operation_id}")

    def get_operation(self, operation_id: str) -> GetOperationResponseDict:
        """ получение ответа на запрос информации об операции"""
        response = self.get_operation_api(operation_id)
        return response.json()

    def make_fee_operation_api(self, request: MakeFeeOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для cоздания операции комиссии.
        :param request: Словарь с status, amount, cardId, accountId:.
        :return: Объект httpx.Response с результатом операции.
         """
        return self.post("/api/v1/operations/make-fee-operation", json=request)

    def make_fee_operation(self, card_id: str, account_id: str) -> MakeFeeOperationResponseDict:
        request = MakeFeeOperationRequestDict(
            status="COMPLETED",
            amount=55.77,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_fee_operation_api(request)
        return response.json()

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции пополнения.
        :param request: Словарь с status, amount, cardId, accountId:.
        :return: Объект httpx.Response с результатом операции.
         """
        return self.post("/api/v1/operations/make-top-up-operation", json=request)

    def make_top_up_operation(self, card_id: str, account_id: str) -> MakeTopUpOperationResponseDict:
        request = MakeTopUpOperationRequestDict(
            status="COMPLETED",
            amount=66.77,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_top_up_operation_api(request)
        return response.json()

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания  операции кэшбэка.
        :param request: Словарь с status, amount, cardId, accountId:.
        :return: Объект httpx.Response с результатом операции.
         """
        return self.post("/api/v1/operations/make-cashback-operation", json=request)

    def make_cashback_operation(self, card_id: str, account_id: str) -> MakeCashbackOperationResponseDict:
        request = MakeCashbackOperationRequestDict(
            status="COMPLETED",
            amount=77.77,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_cashback_operation_api(request)
        return response.json()

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания  операции перевода.
        :param request: Словарь с status, amount, cardId, accountId:.
        :return: Объект httpx.Response с результатом операции.
         """
        return self.post("/api/v1/operations/make-transfer-operation", json=request)

    def make_transfer_operation(self, card_id: str, account_id: str) -> MakeTransferOperationResponseDict:
        request = MakeTransferOperationRequestDict(
            status="COMPLETED",
            amount=88.77,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_transfer_operation_api(request)
        return response.json()

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания  операции покупки.
        :param request: cловарь с status, amount, cardId, accountId, category.
        :return: Объект httpx.Response с результатом операции.
         """
        return self.post("/api/v1/operations/make-purchase-operation", json=request)

    def make_purchase_operation(self, card_id: str, account_id: str, category: str) -> MakePurchaseOperationResponseDict:
        request = MakePurchaseOperationRequestDict(
            status="COMPLETED",
            amount=99.77,
            cardId=card_id,
            accountId=account_id,
            category=category
        )
        response = self.make_purchase_operation_api(request)
        return response.json()

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания  операции оплаты по счету.
        :param request: Словарь с status, amount, cardId, accountId.
        :return: Объект httpx.Response с результатом операции.
         """
        return self.post("/api/v1/operations/make-bill-payment-operation", json=request)

    def make_bill_payment_operation(self, card_id: str, account_id: str) -> MakeBillPaymentOperationResponseDict:
        request = MakeBillPaymentOperationRequestDict(
            status="COMPLETED",
            amount=88.77,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_bill_payment_operation_api(request)
        return response.json()

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания  операции снятия наличных денег.
        :param request: Словарь с status, amount, cardId, accountId.
        :return: Объект httpx.Response с результатом операции.
         """
        return self.post("/api/v1/operations/make-cash-withdrawal-operation", json=request)

    def make_cash_withdrawal_operation(self, card_id: str, account_id: str) -> MakeCashWithdrawalOperationResponseDict:
        request = MakeCashWithdrawalOperationRequestDict(
            status="COMPLETED",
            amount=88.77,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_cash_withdrawal_operation_api(request)
        return response.json()


def build_operations_gateway_http_client() -> OperationsGatewayHTTPClient:
    """
    Функция создаёт экземпляр OperationsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию OperationsGatewayHTTPClient.
    """
    return OperationsGatewayHTTPClient(client=build_gateway_http_client())
