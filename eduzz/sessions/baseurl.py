from urllib.parse import urljoin

from eduzz.sessions.base import BaseSession


class BaseUrlSession(BaseSession):
    """Taken from https://github.com/requests/toolbelt/"""

    def __init__(self, base_url="", **kwargs):
        self.base_url = base_url
        super(BaseUrlSession, self).__init__(**kwargs)

    def prepare_request(self, request):
        """Prepare the request after generating the complete URL."""
        request.url = urljoin(self.base_url, request.url)
        return super(BaseUrlSession, self).prepare_request(request)
