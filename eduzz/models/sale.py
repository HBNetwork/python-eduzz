from datetime import datetime, date
from enum import Enum
from typing import Any, Optional

from attrs import define

from eduzz.converters import converter
from eduzz.types import Money


class Days(Enum):
    um = 1
    sete = 7
    quinze = 15
    trinta = 30
    sessenta = 60


class SaleDateType(Enum):
    creation = "creation"
    payment = "payment"
    update = "update"
    due = "due"


class SaleStatus(Enum):
    Aberta = 1
    Paga = 3
    Cancelada = 4
    AguardandoReembolso = 6
    Reembolsado = 7
    Duplicada = 9
    Explirada = 10
    EmRecuperacao = 11
    AguardandoPagamento = 15


@define
class SaleAmount:
    date: date
    sale_discount: Money
    sale_amount_win: Money
    sale_net_gain: Money
    sale_coop: Money
    sale_partner: Money
    sale_fee: Money
    sale_others: Money
    sale_total: Money


@define
class InvoiceItem:
    invoice_item_id: int
    invoice_id: int
    invoice_item_description: str
    invoice_item_value: Money
    invoice_item_date_create: datetime
    invoice_item_product_id: int
    invoice_item_unit_value: int
    invoice_item_quantity: int
    invoice_item_content_id: int
    invoice_item_discount_value: Money
    invoice_item_freight_type: Any
    invoice_item_freight_deadline: Any
    invoice_order_id: int
    tracking_code: str


@define
class Sale:
    affiliate_id: int
    affiliate_name: Any  # ?
    client_cel: str  # ddd+phone
    client_document: str  # cpf/cnpj
    client_email: str  # email
    client_first_access_id: Any  # ?
    client_id: int
    client_name: str
    content_id: int
    content_title: str
    content_type_id: int  # ? enum
    contract_id: Optional[int]
    date_create: datetime
    date_payment: datetime
    date_update: datetime
    due_date: datetime
    installments: Optional[int]
    producer_id: int
    producer_name: str
    refund_partial_value: Any  # ?
    refund_type: Any  # ?
    refund_value: Any  # ?
    sale_amount_win: Money
    sale_coop: Money
    sale_fee: Optional[Money]
    sale_funil_infinito: Optional[int]
    sale_id: int
    sale_item_discount: Money
    sale_item_id: int
    sale_net_gain: Money
    sale_others: Money
    sale_partner: Money
    sale_payment_method: str
    sale_recuperacao: int  # ?
    sale_status: SaleStatus
    sale_total: Money
    sku: Any
    tracker2: Any
    tracker3: Any
    tracker: Any
    utm_campaign: Any
    utm_content: Any
    utm_medium: Any
    utm_source: Any


if __name__ == "__main__":

    data = {
        "sale_id": 29815013,
        "contract_id": 1393571,
        "due_date": "2021-12-02 16:19:06.000",
        "date_create": "2021-11-30 16:19:06.000",
        "date_payment": "2021-11-30 16:19:09.000",
        "date_update": "2021-11-30 16:19:25.000",
        "sale_status": 3,
        "sale_status_name": "Paga",
        "sale_item_id": 31266972,
        "sale_item_discount": ".00",
        "client_first_access_id": None,
        "sale_recuperacao": 0,
        "sale_funil_infinito": 0,
        "sale_amount_win": "31.24",
        "sale_net_gain": "31.24",
        "sale_coop": ".00",
        "sale_partner": ".00",
        "sale_fee": "-2.66",
        "sale_others": ".00",
        "sale_total": "33.90",
        "refund_type": None,
        "refund_value": None,
        "refund_partial_value": None,
        "sale_payment_method": "Mastercard",
        "client_id": 46360073,
        "client_name": "FIRST LAST",
        "client_email": "firt@email.com",
        "client_document": "01234567890",
        "client_cel": "21996186180",
        "producer_id": 552562,
        "affiliate_id": 0,
        "producer_name": "Henrique Bastos",
        "affiliate_name": None,
        "utm_source": None,
        "utm_campaign": None,
        "utm_medium": None,
        "utm_content": None,
        "tracker": None,
        "tracker2": None,
        "tracker3": None,
        "content_id": 810787,
        "content_title": "Clube de Programadores Python -  Mensal",
        "content_type_id": 1,
        "sku": None,
        "installments": 1,
    }
    obj = converter.structure(data, Sale)
    print(obj)
