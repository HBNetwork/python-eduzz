from functools import cache

from requests import Response
from requests.exceptions import InvalidJSONError

import jsonplus
from requests_customjson.base_session import BaseSession


class JsonResponse(Response):
    """A Response class for requests that knows its json decoder."""

    def __init__(self, json_decoder=None):
        self.json_decoder = json_decoder
        super().__init__()

    @cache
    def json(self, **kwargs):
        """Decodes data with custom json decoder and caches the resulting dictionary."""
        kwargs.setdefault("cls", self.json_decoder)
        return super().json(**kwargs)


class JsonSession(BaseSession):
    """Allows for customization of json encoding, decoding, and Response subclass."""

    JSON_ENCODER = jsonplus.JSONEncoderPlus
    JSON_DECODER = jsonplus.JSONDecoderPlus
    RESPONSE_CLASS = JsonResponse
    REQUEST_BODY_ENCODING = "utf-8"
    REQUEST_CONTENT_TYPE = "application/json"

    def __init__(
        self,
        json_encoder=None,
        json_decoder=None,
        response_class=None,
        request_body_encoding=None,
        request_content_type=None,
        **kwargs
    ):
        self.json_encoder = json_encoder or self.JSON_ENCODER
        self.json_decoder = json_decoder or self.JSON_DECODER
        self.response_class = response_class or self.RESPONSE_CLASS
        self.request_body_encoding = request_body_encoding or self.REQUEST_BODY_ENCODING
        self.request_content_type = request_content_type or self.REQUEST_CONTENT_TYPE

        super().__init__(**kwargs)

    def request(self, *args, **kwargs):
        """Override requests.Session.request to ensure the response will behave as our custom Response class."""
        response = super().request(*args, **kwargs)
        response = self.cast_response(response, self.response_class, self.json_decoder)
        return response

    @staticmethod
    def cast_response(response, response_class, json_decoder):
        """Smelly magic to force the response object to user our Response class conde."""
        response.__class__ = response_class
        response.json_decoder = json_decoder
        return response

    def prepare_request(self, request):
        """Override of requests.Session.prepare_request to ensure json is encoded with our custom encoder.

        This is how requests turn a json dictionary into data bytes:

        1. requests.Session.request will call requests.Session.prepare_request to build the actual request details.
        2. requests.Session.prepare_request will instantiate a PrepareRequest objects.
        3. PrepareRequest.prepare will do the heavy lifting, and at some point will call PrepareRequest.prepare_body
        4. PrepareRequest.prepare_body will encode the json to bytes and set request.data if data is not defined.

        Before requests.Session.prepare_request is called, we anticipate and encode json with our custom encoder
        and
        provide the results as request.data bypassing PrepareRequest.prepare_body encoding process.
        """
        self.before_prepare_body(request)
        return super().prepare_request(request)

    def before_prepare_body(self, request):
        """Encode json using custom encoder before PrepareRequest.prepare_body is called."""

        # When Request has data but no json, there is nothing to encode.
        if request.data and request.json is None:
            return

        # Snippet from requests.PreparedRequest.prepare_body
        try:
            data = jsonplus.dumps(request.json, allow_nan=False, cls=self.JSON_ENCODER)
        except ValueError as ve:
            raise InvalidJSONError(ve, request=self) from ve

        if not isinstance(data, bytes):
            data = data.encode(self.REQUEST_BODY_ENCODING)

        request.data = data
        request.json = None

        # Ensure request has a content-type.
        if "content-type" not in request.headers:
            request.headers["Content-Type"] = self.REQUEST_CONTENT_TYPE
