from datetime import date
from functools import partial

import pytest

import jsonplus as json
from eduzz.client import EduzzClient
from eduzz.session import EduzzSession


class TestServiceSale:
    @pytest.fixture
    def eduzz(self):
        return EduzzClient(EduzzSession())

    def test_get_sale(self, responses, eduzz):
        responses.add(responses.GET, "/sale/get_sale/1", json=sample_get_sale_200(), status=200)
        sale = eduzz.sale.get_sale(1)
        assert sale.sale_id == 123456

    def test_get_sale_list_with_2_pages(self, responses, eduzz):
        add = partial(responses.add, responses.GET, "/sale/get_sale_list", status=200)
        add(json=sample_get_sale_list_200_page1())
        add(json=sample_get_sale_list_200_page2())

        sales = eduzz.sale.get_sale_list(date(2020, 9, 28), date(2020, 9, 28))
        assert [s.sale_id for s in sales] == [1, 2, 3, 4]


def sample_get_sale_200():
    return json.loads(
        """
        {
        "success": true,
        "data": [
            {
                "sale_id": 123456,
                "contract_id": 2098111,
                "date_create": "2018-04-23 13:44:54.873",
                "date_payment": null,
                "date_update": "2018-04-23 13:44:54.873",
                "sale_status": 4,
                "sale_status_name": "Cancelada",
                "sale_item_id": 321654,
                "sale_item_discount": ".00",
                "client_first_access_id": null,
                "sale_recuperacao": 0,
                "sale_funil_infinito": 0,
                "sale_amount_win": null,
                "installments": 1,
                "sale_net_gain": null,
                "sale_coop": ".00",
                "sale_partner": ".00",
                "sale_fee": null,
                "sale_others": null,
                "sale_total": "22.00",
                "refund_type": "parcial",
                "refund_value": 22,
                "refund_partial_value": 10,
                "sale_payment_method": "Boleto Banc\u00e1rio",
                "client_id": 10091151,
                "client_name": "Client Name",
                "client_email": "client@email.com",
                "client_document": "08768617372",
                "client_street": "Rua Fulano de Tal",
                "client_addressnumber": 90,
                "client_complement": "Complemento",
                "client_neighborhood": "Bairro",
                "client_zip_code": "00000-000",
                "client_city": "Sao Paulo",
                "client_district": "SP",
                "client_telephone": "(11) 0000-0000",
                "client_telephone2": "(11) 0000-0000",
                "client_cel": "(11) 0000-0000",
                "producer_id": 1233455,
                "affiliate_id": 353821,
                "producer_name": "Producer Name",
                "affiliate_name": "Afiliado da Silva",
                "utm_source": null,
                "utm_campaign": null,
                "utm_medium": null,
                "utm_content": null,
                "tracker": "123",
                "content_id": 757,
                "content_title": "Content Example 1",
                "content_type_id": 1,
                "card_number": "4063********9635",
                "due_date": "2018-04-23 13:44:54.873",
                "invoice_items": [
                    {
                        "invoice_item_id": 2165818,
                        "invoice_item_description": "Item example",
                        "invoice_item_unit_value": 80,
                        "invoice_item_quantity": 1,
                        "invoice_item_value": 80,
                        "invoice_item_discount_value": 20,
                        "invoice_item_freight_type": null,
                        "invoice_item_freight_deadline": null,
                        "invoice_item_content_id": 1231241,
                        "tracking_code": null
                    }
                ],
                "sale_coop_detail": [
                    {
                        "coproducer_id": 123,
                        "coproducer_email": "producer@mail.com",
                        "coproducer_name": "Carl Jacob",
                        "sale_net_gain": 20.3,
                        "is_affiliate_manager": 1
                    }
                ],
                "sale_affiliate_detail": [
                    {
                        "affiliate_id": 353821,
                        "affiliate_email": "afiliado@mail.com",
                        "affiliate_name": "Afiliado da Silva",
                        "sale_net_gain": 20.3
                    }
                ],
                "recipient": {
                    "recipient_id": 123456,
                    "recipient_name": "Recipient Name",
                    "recipient_email": "Recipient Email",
                    "recipient_document": 12345678900,
                    "recipient_cel": 1500000000
                }
            }
        ],
        "profile": {
            "start": 1526058863.48454,
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVC89.eyJhdWQiOiIzZDc3YzlmOGIxIiwiZXhwIjo5MDAsImlhdCI6MTUzMjUzNzk0MSwiaXNzIjoibXllZHV6ei1hcGktdXNlciIsInN1YiI6ODE1OTU5fQ==.JomRnis4AEOTj5PPST90V1Q/z7fPhOGVnkKAQ2j6mOc=",
            "token_valid_until": "2018-07-25 17:14:01",
            "finish": 1526058864.089432,
            "process": 0.6048920154571533
        }
    }
    """
    )


def sample_get_sale_list_200_page1():
    return json.loads(
        """
        {
            "success": true,
            "data": [
                {
                    "sale_id": 1,
                    "contract_id": 654321,
                    "date_create": "2018-04-23 13:44:54.873",
                    "date_payment": null,
                    "date_update": "2018-04-23 13:44:54.873",
                    "due_date": "2018-04-23 13:44:54.873",
                    "sale_status": 4,
                    "sale_status_name": "Cancelada",
                    "sale_item_id": 321654,
                    "sale_item_discount": ".00",
                    "client_first_access_id": null,
                    "sale_recuperacao": 0,
                    "sale_funil_infinito": 0,
                    "sale_amount_win": null,
                    "sale_net_gain": null,
                    "sale_coop": ".00",
                    "sale_partner": ".00",
                    "sale_fee": null,
                    "sale_others": null,
                    "sale_total": "22.00",
                    "sale_payment_method": "Boleto Banc\u00e1rio",
                    "client_id": 10091151,
                    "client_name": "Client Name",
                    "client_email": "client@email.com",
                    "client_document": "08768617372",
                    "client_cel": "15998350954",
                    "producer_id": 1233455,
                    "affiliate_id": 353821,
                    "producer_name": "Producer Name",
                    "affiliate_name": "Afiliate Name",
                    "utm_source": null,
                    "utm_campaign": null,
                    "utm_medium": null,
                    "utm_content": null,
                    "tracker": "123",
                    "content_id": 757,
                    "content_title": "Content Example 1",
                    "content_type_id": 1,
                    "installments": 1
                },
                {
                    "sale_id": 2,
                    "contract_id": null,
                    "date_create": "2018-04-22 13:44:54.873",
                    "date_payment": null,
                    "date_update": "2018-04-22 13:44:54.873",
                    "due_date": "2018-04-22 13:44:54.873",
                    "sale_status": 4,
                    "sale_status_name": "Cancelada",
                    "sale_item_id": 321655,
                    "sale_item_discount": ".00",
                    "client_first_access_id": null,
                    "sale_recuperacao": 0,
                    "sale_funil_infinito": 0,
                    "sale_amount_win": null,
                    "sale_net_gain": null,
                    "sale_coop": ".00",
                    "sale_partner": ".00",
                    "sale_fee": null,
                    "sale_others": null,
                    "sale_total": "522.00",
                    "refund_type": "parcial",
                    "refund_value": 522,
                    "refund_partial_value": 250,
                    "sale_payment_method": "Boleto Banc\u00e1rio",
                    "client_id": 10091151,
                    "client_name": "Client Name",
                    "client_email": "client@email.com",
                    "client_document": "08768617372",
                    "client_cel": "15998350954",
                    "producer_id": 1233455,
                    "affiliate_id": 353821,
                    "producer_name": "Producer Name",
                    "affiliate_name": "Afiliate Name",
                    "utm_source": null,
                    "utm_campaign": null,
                    "utm_medium": null,
                    "utm_content": null,
                    "tracker": 456,
                    "content_id": 757,
                    "content_title": "Content Example 1",
                    "content_type_id": 1,
                    "installments": 1
                }
            ],
            "profile": {
                "start": 1526058863.48454,
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVC89.eyJhdWQiOiIzZDc3YzlmOGIxIiwiZXhwIjo5MDAsImlhdCI6MTUzMjUzNzk0MSwiaXNzIjoibXllZHV6ei1hcGktdXNlciIsInN1YiI6ODE1OTU5fQ==.JomRnis4AEOTj5PPST90V1Q/z7fPhOGVnkKAQ2j6mOc=",
                "token_valid_until": "2018-07-25 17:14:01",
                "finish": 1526058864.089432,
                "process": 0.6048920154571533
            },
            "paginator": {
                "page": 1,
                "size": 2,
                "totalPages": 2,
                "totalRows": 4
            }
        }
        """
    )


def sample_get_sale_list_200_page2():
    return json.loads(
        """
        {
            "success": true,
            "data": [
                {
                    "sale_id": 3,
                    "contract_id": 654321,
                    "date_create": "2018-04-23 13:44:54.873",
                    "date_payment": null,
                    "date_update": "2018-04-23 13:44:54.873",
                    "due_date": "2018-04-23 13:44:54.873",
                    "sale_status": 4,
                    "sale_status_name": "Cancelada",
                    "sale_item_id": 321654,
                    "sale_item_discount": ".00",
                    "client_first_access_id": null,
                    "sale_recuperacao": 0,
                    "sale_funil_infinito": 0,
                    "sale_amount_win": null,
                    "sale_net_gain": null,
                    "sale_coop": ".00",
                    "sale_partner": ".00",
                    "sale_fee": null,
                    "sale_others": null,
                    "sale_total": "22.00",
                    "sale_payment_method": "Boleto Banc\u00e1rio",
                    "client_id": 10091151,
                    "client_name": "Client Name",
                    "client_email": "client@email.com",
                    "client_document": "08768617372",
                    "client_cel": "15998350954",
                    "producer_id": 1233455,
                    "affiliate_id": 353821,
                    "producer_name": "Producer Name",
                    "affiliate_name": "Afiliate Name",
                    "utm_source": null,
                    "utm_campaign": null,
                    "utm_medium": null,
                    "utm_content": null,
                    "tracker": "123",
                    "content_id": 757,
                    "content_title": "Content Example 1",
                    "content_type_id": 1,
                    "installments": 1
                },
                {
                    "sale_id": 4,
                    "contract_id": null,
                    "date_create": "2018-04-22 13:44:54.873",
                    "date_payment": null,
                    "date_update": "2018-04-22 13:44:54.873",
                    "due_date": "2018-04-22 13:44:54.873",
                    "sale_status": 4,
                    "sale_status_name": "Cancelada",
                    "sale_item_id": 321655,
                    "sale_item_discount": ".00",
                    "client_first_access_id": null,
                    "sale_recuperacao": 0,
                    "sale_funil_infinito": 0,
                    "sale_amount_win": null,
                    "sale_net_gain": null,
                    "sale_coop": ".00",
                    "sale_partner": ".00",
                    "sale_fee": null,
                    "sale_others": null,
                    "sale_total": "522.00",
                    "refund_type": "parcial",
                    "refund_value": 522,
                    "refund_partial_value": 250,
                    "sale_payment_method": "Boleto Banc\u00e1rio",
                    "client_id": 10091151,
                    "client_name": "Client Name",
                    "client_email": "client@email.com",
                    "client_document": "08768617372",
                    "client_cel": "15998350954",
                    "producer_id": 1233455,
                    "affiliate_id": 353821,
                    "producer_name": "Producer Name",
                    "affiliate_name": "Afiliate Name",
                    "utm_source": null,
                    "utm_campaign": null,
                    "utm_medium": null,
                    "utm_content": null,
                    "tracker": 456,
                    "content_id": 757,
                    "content_title": "Content Example 1",
                    "content_type_id": 1,
                    "installments": 1
                }
            ],
            "profile": {
                "start": 1526058863.48454,
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVC89.eyJhdWQiOiIzZDc3YzlmOGIxIiwiZXhwIjo5MDAsImlhdCI6MTUzMjUzNzk0MSwiaXNzIjoibXllZHV6ei1hcGktdXNlciIsInN1YiI6ODE1OTU5fQ==.JomRnis4AEOTj5PPST90V1Q/z7fPhOGVnkKAQ2j6mOc=",
                "token_valid_until": "2018-07-25 17:14:01",
                "finish": 1526058864.089432,
                "process": 0.6048920154571533
            },
            "paginator": {
                "page": 2,
                "size": 2,
                "totalPages": 2,
                "totalRows": 4
            }
        }
        """
    )


def sample_last_days_amount_200():
    return json.loads(
        """
    {
    "success": true,
    "data": [
        {
            "date": "2108-05-06",
            "sale_discount": 0,
            "sale_amount_win": 13.54,
            "sale_net_gain": 87.23,
            "sale_coop": 0,
            "sale_partner": -244.46,
            "sale_fee": -0.05,
            "sale_others": 0,
            "sale_total": 22
        },
        {
            "date": "2108-05-05",
            "sale_discount": 0,
            "sale_amount_win": 13.54,
            "sale_net_gain": 87.23,
            "sale_coop": 0,
            "sale_partner": -244.46,
            "sale_fee": -0.05,
            "sale_others": 0,
            "sale_total": 22
        }
    ],
    "profile": {
        "start": 1526058863.48454,
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVC89.eyJhdWQiOiIzZDc3YzlmOGIxIiwiZXhwIjo5MDAsImlhdCI6MTUzMjUzNzk0MSwiaXNzIjoibXllZHV6ei1hcGktdXNlciIsInN1YiI6ODE1OTU5fQ==.JomRnis4AEOTj5PPST90V1Q/z7fPhOGVnkKAQ2j6mOc=",
        "token_valid_until": "2018-07-25 17:14:01",
        "finish": 1526058864.089432,
        "process": 0.6048920154571533
    }
}   """
    )
