from pydantic import BaseModel, HttpUrl


class DocumentSchema(BaseModel):
    #Добавили суффикс Schema вместо Dict. Наследуем от BaseModel вместо TypedDict
    """
    Описание структуры документа.
    """
    url: HttpUrl
    document: str #здесь же алиас не нужен, в любых case слово document одинаково пишется


class GetTariffDocumentResponseSchema(BaseModel):
    """
    описание структуры ответа создания документа по тарифу
    """
    tariff: DocumentSchema


class GetContractDocumentResponseSchema(BaseModel):
    """
    описание структуры ответа создания документа по контракту
    """
    contract: DocumentSchema

