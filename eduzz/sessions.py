from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter


class BaseUrlSession(requests.Session):
    """Taken from https://github.com/requests/toolbelt/"""

    def __init__(self, base_url):
        self.base_url = base_url
        super(BaseUrlSession, self).__init__()

    def prepare_request(self, request):
        """Prepare the request after generating the complete URL."""
        request.url = urljoin(self.base_url, request.url)
        return super(BaseUrlSession, self).prepare_request(request)


class EduzzAPIError(requests.HTTPError):
    """An API level error has ocurred."""


class EduzzResponse(requests.Response):
    ERROR_STATUSES = {400, 401, 403, 404, 405, 409, 422, 500}

    def __init__(self):
        self._json = None
        super(EduzzResponse, self).__init__()

    def __repr__(self):
        return "<Response [%s] %s>" % (self.status_code, self.url)

    @classmethod
    def from_response(cls, r):
        """Smelly magic to circunvent requests coupling to it's own Response class."""
        r.__class__ = cls
        r._json = None  # Necessary because we can't run __init__ again.
        return r

    def raise_for_status(self):
        if self.status_code in self.ERROR_STATUSES:
            json = self.json()
            code, details = json["code"], json["details"]

            raise EduzzAPIError(f"{code} {details}", response=self)

        super(EduzzResponse, self).raise_for_status()

    def json(self, **kwargs):
        if self._json is None:
            self._json = super(EduzzResponse, self).json(**kwargs)

        return self._json


class EduzzAdapter(HTTPAdapter):
    def __init__(self, response_factory=EduzzResponse.from_response, **kwargs):
        self.response_factory = response_factory
        super(EduzzAdapter, self).__init__(**kwargs)

    def send(self, *args, **kwargs):
        r = super(EduzzAdapter, self).send(*args, **kwargs)
        return self.response_factory(r)


class EduzzSession(BaseUrlSession):
    ENDPOINT = "https://api2.eduzz.com/"

    def __init__(self):
        super(EduzzSession, self).__init__(base_url=self.ENDPOINT)
        self.mount(self.ENDPOINT, EduzzAdapter())
