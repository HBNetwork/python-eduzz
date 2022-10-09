from eduzz.client.financial import FinancialClient
from eduzz.client.sale import SaleClient
from eduzz.session import EduzzSession


class EduzzClient:
    def __init__(self, session):
        self.session = session
        self.sale = SaleClient(self)
        self.financial = FinancialClient(self)

    @classmethod
    def from_credentials(cls, **credentials):
        session = EduzzSession.from_credentials(**credentials)
        return cls(session)

    def get_all(self, path, params):
        for r in self.session.get_all(path, params=params):
            r.raise_for_status()
            yield r.json()["data"]

    def request(self, method, path, params):
        r = self.session.request(method, path, params)
        r.raise_for_status()
        return r.json()["data"]

    def get(self, path, params=None):
        return self.request("GET", path, params=params)

    def post(self, path, params=None):
        return self.request("POST", path, params=params)
