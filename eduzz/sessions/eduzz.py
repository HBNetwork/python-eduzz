from requests import HTTPError

from eduzz.sessions import EduzzAuth
from eduzz.sessions.baseurl import BaseUrlSession
from eduzz.sessions.customjson import JsonResponse, JsonSession


class EduzzAPIError(HTTPError):
    """An API level error has ocurred."""


class EduzzResponse(JsonResponse):
    ERROR_STATUSES = {400, 401, 403, 404, 405, 409, 422, 500}

    def __repr__(self):
        return "<Response [%s] %s>" % (self.status_code, self.url)

    def raise_for_status(self):
        if self.status_code in self.ERROR_STATUSES:
            json = self.json()
            code, details = json["code"], json["details"]

            raise EduzzAPIError(f"{code} {details}", response=self)

        super(EduzzResponse, self).raise_for_status()


class EduzzSession(JsonSession, BaseUrlSession):
    """Full featured session to work with high level clients."""

    ENDPOINT = "https://api2.eduzz.com"
    RESPONSE_CLASS = EduzzResponse

    def __init__(
        self,
        base_url="",
        json_encoder=None,
        json_decoder=None,
        response_class=None,
        **kwargs,
    ):
        super(EduzzSession, self).__init__(
            base_url=base_url or self.ENDPOINT,
            json_encoder=json_encoder,
            json_decoder=json_decoder,
            response_class=response_class,
            **kwargs,
        )

    @classmethod
    def from_credentials(cls, email, publickey, apikey, **httpadapter_kwargs):
        self = cls(**httpadapter_kwargs)
        self.auth = EduzzAuth(email, publickey, apikey, EduzzSession)
        return self
