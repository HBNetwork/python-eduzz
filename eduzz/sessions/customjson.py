import json as json_module
from functools import cache, partial

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import InvalidJSONError

from eduzz.serializers import BetterJSONEncoder, BetterJSONDecoder
from eduzz.sessions.base import BaseSession


class JsonResponse(requests.Response):
    """
    This class is a proper Response subclass that contemplates the API's design decisions.
    This could be an adapter, but we would hit __getattr__ everytime.
    """

    def __init__(self):
        self.json_decoder = None
        super(JsonResponse, self).__init__()

    @classmethod
    def cast(cls, r, json_decoder=None):
        """Smelly magic to circunvent requests coupling to it's own Response class."""
        r.__class__ = cls
        r.json_decoder = json_decoder
        return r

    @cache
    def json(self, **kwargs):
        kwargs.setdefault("cls", self.json_decoder)
        return super(JsonResponse, self).json(**kwargs)


class JsonAdapter(HTTPAdapter):
    def __init__(self, response_factory, **kwargs):
        self.response_factory = response_factory
        super(JsonAdapter, self).__init__(**kwargs)

    def send(self, *args, **kwargs):
        r = super(JsonAdapter, self).send(*args, **kwargs)
        return self.response_factory(r)


class JsonSession(BaseSession):
    JSON_ENCODER = BetterJSONEncoder
    JSON_DECODER = BetterJSONDecoder
    RESPONSE_CLASS = JsonResponse

    def __init__(
        self,
        json_encoder=None,
        json_decoder=None,
        response_class=None,
        **kwargs
    ):
        self.json_encoder = json_encoder or self.JSON_ENCODER
        self.json_decoder = json_decoder or self.JSON_DECODER
        self.response_class = response_class or self.RESPONSE_CLASS

        super(JsonSession, self).__init__(**kwargs)

        factory = partial(
            self.response_class.cast, json_decoder=self.json_decoder
        )
        self.mount("https://", JsonAdapter(response_factory=factory))
        self.mount("http://", JsonAdapter(response_factory=factory))

    def prepare_request(self, request):
        self.switch_json_with_data(request)
        return super(JsonSession, self).prepare_request(request)

    def switch_json_with_data(self, request):
        """All this to make sure WE encode request.json before requests uses
        the original json.JSONEncoder. The cost of not inverting dependencies."""
        if request.data and request.json is None:
            return

        # Snippet from requests.PreparedRequest.prepare_body
        try:
            data = json_module.dumps(
                request.json, allow_nan=False, cls=self.JSON_ENCODER
            )
        except ValueError as ve:
            raise InvalidJSONError(ve, request=self)

        if not isinstance(data, bytes):
            data = data.encode("utf-8")

        # Update request state.
        request.data = data
        if "content-type" not in request.headers:
            request.headers["Content-Type"] = "application/json"
        request.json = None
