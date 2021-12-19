from requests_futures.sessions import FuturesSession

from eduzz.auth import EduzzToken
from eduzz.sessions import EduzzSession


class Eduzz:
    def __init__(self, session):
        self.session = session

    @classmethod
    def from_credentials(cls, **credentials):
        auth = EduzzToken(**credentials)
        session = EduzzSession()
        session.auth = auth

        return cls(session)

    def get_sales_list(self, start_date, end_date):
        next_page = 1

        while next_page:
            params = {"start_date": start_date, "end_date": end_date, "page": next_page}

            response = self.session.get("/sale/get_sale_list", params=params)
            response.raise_for_status()
            json = response.json()

            yield from json["data"]

            paginator = json["paginator"]
            if paginator["page"] >= paginator["totalPages"]:
                break
            next_page += 1

    def get_sales_list2(self, start_date, end_date):
        next_page = 1

        params = {"start_date": start_date, "end_date": end_date, "page": next_page}

        response = self.session.get("/sale/get_sale_list", params=params)
        print(response)
        response.raise_for_status()
        json = response.json()

        paginator = json["paginator"]
        print(paginator)

        with FuturesSession(session=self.session) as session:
            futures = [
                session.get(
                    "/sale/get_sale_list", params={"start_date": start_date, "end_date": end_date, "page": page}
                )
                for page in range(paginator["page"] + 1, paginator["totalPages"] + 1)
            ]

        yield from json["data"]

        for future in futures:
            response = future.result()
            print(response)
            json = response.json()
            yield from json["data"]
