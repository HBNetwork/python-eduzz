import json as json_module
from functools import partial

from requests.exceptions import InvalidJSONError

from jsonplus import JSONDecoderPlus, JSONEncoderPlus

from .adapters import JsonAdapter
from .base import BaseSession
from .models import JsonResponse


class JsonSession(BaseSession):
    JSON_ENCODER = JSONEncoderPlus
    JSON_DECODER = JSONDecoderPlus
    RESPONSE_CLASS = JsonResponse

    def __init__(self, json_encoder=None, json_decoder=None, response_class=None, **kwargs):
        self.json_encoder = json_encoder or self.JSON_ENCODER
        self.json_decoder = json_decoder or self.JSON_DECODER
        self.response_class = response_class or self.RESPONSE_CLASS

        super(JsonSession, self).__init__(**kwargs)

        factory = partial(self.response_class.cast, json_decoder=self.json_decoder)
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
            data = json_module.dumps(request.json, allow_nan=False, cls=self.JSON_ENCODER)
        except ValueError as ve:
            raise InvalidJSONError(ve, request=self)

        if not isinstance(data, bytes):
            data = data.encode("utf-8")

        # Update request state.
        request.data = data
        if "content-type" not in request.headers:
            request.headers["Content-Type"] = "application/json"
        request.json = None
