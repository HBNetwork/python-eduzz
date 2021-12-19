from urllib.parse import urljoin

import requests

from eduzz.adapters import EduzzAdapter
from eduzz.adapters import EduzzAPIError  # noqa
from eduzz.auth import EduzzAuth


class BaseUrlSession(requests.Session):
    """Taken from https://github.com/requests/toolbelt/"""

    def __init__(self, base_url):
        self.base_url = base_url
        super(BaseUrlSession, self).__init__()

    def prepare_request(self, request):
        """Prepare the request after generating the complete URL."""
        request.url = urljoin(self.base_url, request.url)
        return super(BaseUrlSession, self).prepare_request(request)


class EduzzBaseSession(BaseUrlSession):
    """Knows how navigate on Eduzz API V2. Used by EduzzAuth token generation."""

    ENDPOINT = "https://api2.eduzz.com/"

    def __init__(self, **httpadapter_kwargs):
        """httpadapter_kwargs can be: pool_connections, pool_maxsize, max_retries, pool_block."""
        super(EduzzBaseSession, self).__init__(base_url=self.ENDPOINT)
        self.mount(self.ENDPOINT, EduzzAdapter(**httpadapter_kwargs))


class EduzzSession(EduzzBaseSession):
    """Full featured session to work with high level clients."""

    @classmethod
    def from_credentials(cls, email, publickey, apikey, **httpadapter_kwargs):
        self = cls(**httpadapter_kwargs)
        self.auth = EduzzAuth(email, publickey, apikey, EduzzBaseSession)
        return self
