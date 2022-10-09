from datetime import date, datetime
from typing import Any, Optional

from attr import define

from money import Money


@define
class PaymentMethod:
    id: int
    customer_id: int
    token: str
    registration_date: datetime
    last_digits: str
    brand: str


@define
class BankAccount:
    id: Optional[int]
    status_id: Optional[int]
    status_name: Optional[str]
    notice: Optional[str]
    date_create: Optional[datetime]
    date_update: Optional[datetime]
    bank_account_id: Optional[int]
    bank_number: str
    bank_name: str
    account_type: str
    agency_number: str
    agency_digit: str
    account_number: str
    account_digit: str
    account_holder_name: str
    account_holder_taxid: str
    account_holder_type: str
    moip_account: Any


@define
class Balance:
    balance: Money
    future_balance: Money


@define
class ValueAvailable:
    value_available: Money
    antecipable: Money


@define
class Transfer:
    tranfer_id: int
    created_date: date
    bank_account_id: int
    type_name: str
    value: Money
    status_name: str
    status_cod: int
    send_date: date
    return_date: date
    return_msg: str


@define
class Statement:
    statement_id: int
    statement_date: date
    statement_description: str
    statement_document: str
    statement_value: Money
