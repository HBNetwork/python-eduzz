from datetime import date

from eduzz.magic import autostructure
from eduzz.models.financial import (
    Balance,
    BankAccount,
    PaymentMethod,
    Statement,
    Transfer,
    ValueAvailable,
)
from eduzz.services.base import BaseService


class FinancialService(BaseService):
    @autostructure
    def payment_methods(self, page: int | None = None) -> list[PaymentMethod]:
        yield from self.client.get_all("/sale/get_sale_list", params=self.params())

    @autostructure
    def bank_details(self) -> BankAccount:
        return self.client.get("/financial/bank_details", params=self.params())

    @autostructure
    def balance(self) -> Balance:
        return self.client.get("/financial/balance")

    @autostructure
    def fund_transfer_methods(self, page: int | None = None) -> list[BankAccount]:
        yield from self.client.get_all("/financial/fund_transfer_method", params=self.params())

    @autostructure
    def value_available(self) -> ValueAvailable:
        return self.client.get("/financial/value_available")

    @autostructure
    def transfer_list(self, page: int | None = None) -> list[Transfer]:
        yield from self.client.get_all("/financial/transfers_list", params=self.params())

    def can_request_bank_transfer(self):
        data = self.client.get("/financial/can_request_bank_transfer")
        return data["permission"]

    @autostructure
    def statement(self, start_date: date, end_date: date, page: int | None = None) -> list[Statement]:
        yield from self.client.get_all("/financial/statement", params=self.params())
