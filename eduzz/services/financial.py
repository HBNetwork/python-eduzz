from datetime import date
from typing import Optional, List, Generator

from eduzz.converters import converter
from eduzz.models.financial import (
    PaymentMethod,
    BankAccount,
    Balance,
    ValueAvailable,
    Transfer,
    Statement,
)
from eduzz.services.base import Service


class FinancialService(Service):
    def payment_methods(self, page: Optional[int] = None):
        path = "/sale/get_sale_list"
        params = self.params_filtered(self.payment_methods, locals())

        for data in self.client.get_all(path, params=params):
            yield from converter.structure(data, List[PaymentMethod])

    def bank_details(self):
        path = "/financial/bank_details"
        data = self.client.get(path)
        return converter.structure(data, BankAccount)

    def balance(self):
        path = "/financial/balance"
        data = self.client.get(path)
        return converter.structure(data, Balance)

    def fund_transfer_methods(self, page: Optional[int] = None):
        path = "/financial/fund_transfer_method"

        params = {}
        if page:
            params["page"] = page

        for data in self.client.get_all(path, params=params):
            yield from converter.structure(data, List[BankAccount])

    def value_available(self):
        path = "/financial/value_available"
        data = self.client.get(path)
        return converter.structure(data, ValueAvailable)

    def transfer_list(self, page: Optional[int] = None):
        path = "/financial/transfers_list"
        params = {}
        if page:
            params["page"] = page

        for data in self.client.get_all(path, params=params):
            yield from converter.structure(data, List[Transfer])

    def can_request_bank_transfer(self):
        path = "/financial/can_request_bank_transfer"
        data = self.client.get(path)
        return data["permission"]

    def statement(
        self, start_date: date, end_date: date, page: Optional[int] = None
    ) -> Generator[Statement]:
        path = "/financial/statement"

        params = self.params_filtered(self.statement, locals())

        for data in self.client.get_all(path, params=params):
            yield from converter.structure(data, List[Statement])
