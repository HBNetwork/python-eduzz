from urllib.parse import urljoin

import requests


class BaseUrlSession(requests.Session):
    """Taken from https://github.com/requests/toolbelt/"""

    def __init__(self, base_url=""):
        self.base_url = base_url
        super(BaseUrlSession, self).__init__()

    def prepare_request(self, request):
        """Prepare the request after generating the complete URL."""
        request.url = urljoin(self.base_url, request.url)
        return super(BaseUrlSession, self).prepare_request(request)
