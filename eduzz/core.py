from eduzz.sessions import EduzzSession


class Eduzz:
    def __init__(self, session):
        self.session = session

    @classmethod
    def from_credentials(cls, **credentials):
        session = EduzzSession.from_credentials(**credentials)
        return cls(session)

    def get_sales_list(self, start_date, end_date):
        for r in self.session.get_all(
            "/sale/get_sale_list",
            parallel=True,
            params={"start_date": start_date, "end_date": end_date},
        ):
            r.raise_for_status()

            yield from (data for data in r.json()["data"])
