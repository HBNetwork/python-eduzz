from requests_customjson.baseurl_session import BaseUrlSession
from requests_customjson.json_session import JsonResponse, JsonSession


class JsonBaseUrlSession(BaseUrlSession, JsonSession):
    """Session that support base url and custom json."""

    pass
