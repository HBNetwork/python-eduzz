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
        request_method = getattr(self.session, method)
        r = request_method(path, params=params)
        r.raise_for_status()
        return r.json()["data"]

    def get(self, path, params):
        return self.session.request("GET", path, params=params)

    def post(self, path, params):
        return self.session.request("POST", path, params=params)
