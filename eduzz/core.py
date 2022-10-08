from eduzz.services.financial import FinancialService
from eduzz.services.sale import SaleService
from eduzz.sessions import EduzzSession


class Eduzz:
    def __init__(self, session):
        self.session = session
        self.sale = SaleService(self)
        self.financial = FinancialService(self)

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
