from datetime import date
from functools import partial
from typing import Generator

from eduzz.converters import converter
from eduzz.magic import autostructure
from eduzz.models.sale import (
    Days,
    InvoiceItem,
    Sale,
    SaleAmount,
    SaleDateType,
    SaleStatus,
)
from eduzz.services.base import BaseService

autostructure = partial(autostructure, converter=converter)
"Configure autostructure to use our custom converter."


class SaleService(BaseService):
    """Namespace for all sale endpoints."""

    def get_sale_list(
        self,
        start_date: date,
        end_date: date,
        page: int | None = None,
        contract_id: int | None = None,
        affiliate_id: int | None = None,
        content_id: int | None = None,
        invoice_status: SaleStatus | None = None,
        client_email: str | None = None,
        date_type: SaleDateType | None = None,
        parallel=True,
    ) -> Generator[Sale, None, None]:
        """See https://api2.eduzz.com/#sale-get-sale-list"""
        for data in self.client.get_all("/sale/get_sale_list", params=self.params()):
            yield from converter.structure(data, list[Sale])

    @autostructure
    def get_sale(self, sale_id: int) -> Sale:
        """See https://api2.eduzz.com/#sale-get-sale"""
        # We are geting 1 sale, but the endpoints returns it on a list.
        data, *_ = self.client.get(f"/sale/get_sale/{sale_id}")
        return data

    @autostructure
    def last_days_amount(
        self,
        days: Days | None = None,
        affiliate_id: int | None = None,
        content_id: int | None = None,
        invoice_status: SaleStatus | None = None,
    ) -> list[SaleAmount]:
        return self.client.get("/sale/last_days_amount", params=self.params())

    @autostructure
    def tracking_code(self, invoice_item_id: int, tracking_code: str) -> InvoiceItem:
        return self.client.post("/sale/tracking_code", params=self.params())

    @autostructure
    def get_total(
        self,
        start_date: date,
        end_date: date,
        contract_id: int | None = None,
        affiliate_id: int | None = None,
        content_id: int | None = None,
        invoice_status: SaleStatus | None = None,
    ) -> SaleAmount:
        return self.client.get("/sale/get_total", params=self.params())

    def sale_refund(self, sale_id):
        data = self.client.post(f"/sale/refund/{sale_id}")
        return data[0]["message"]
