from datetime import date
from typing import Optional, Generator, List

from eduzz.converters import converter
from eduzz.services.base import Service
from eduzz.models.sale import (
    Sale,
    SaleStatus,
    SaleDateType,
    Days,
    SaleAmount,
    InvoiceItem,
)


class SaleService(Service):
    def get_sale_list(
        self,
        start_date: date,
        end_date: date,
        page: Optional[int] = None,
        contract_id: Optional[int] = None,
        affiliate_id: Optional[int] = None,
        content_id: Optional[int] = None,
        invoice_status: Optional[SaleStatus] = None,
        client_email: Optional[str] = None,
        date_type: Optional[SaleDateType] = None,
        parallel=True,
    ) -> Generator[Sale]:

        path = "/sale/get_sale_list"
        params = self.params_filtered(self.get_sale_list, locals())

        for data in self.client.get_all(path, params=params):
            yield from converter.structure(data, List[Sale])

    def get_sale(self, sale_id: int) -> Sale:
        data = self.client.get(f"/sale/get_sale/{sale_id}")
        return converter.structure(data, Sale)

    def last_days_amount(
        self,
        days: Optional[Days] = None,
        affiliate_id: Optional[int] = None,
        content_id: Optional[int] = None,
        invoice_status: Optional[SaleStatus] = None,
    ) -> List[SaleAmount]:

        params = self.params_filtered(self.last_days_amount, locals())
        data = self.client.get("/sale/last_days_amount", params=params)
        return converter.structure(data, List[SaleAmount])

    def tracking_code(
        self, invoice_item_id: int, tracking_code: str
    ) -> InvoiceItem:

        params = self.params_filtered(self.tracking_code, locals())
        data = self.client.post("/sale/tracking_code", params=params)
        return converter.structure(data, InvoiceItem)

    def get_total(
        self,
        start_date: date,
        end_date: date,
        contract_id: Optional[int] = None,
        affiliate_id: Optional[int] = None,
        content_id: Optional[int] = None,
        invoice_status: Optional[SaleStatus] = None,
    ) -> SaleAmount:
        params = self.params_filtered(self.get_total, locals())
        data = self.client.get("/sale/get_total", params=params)
        return converter.structure(data, SaleAmount)

    def sale_refund(self, sale_id) -> str:
        data = self.client.post(f"/sale/refund/{sale_id}")
        return data[0]["message"]
