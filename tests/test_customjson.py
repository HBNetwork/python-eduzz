import json
import re
from datetime import datetime

import pytest

from eduzz.serializers import serialize
from eduzz.sessions.customjson import JsonSession, JsonResponse


def test_session_returns_response_subclass(httpretty):
    httpretty.register_uri(httpretty.GET, re.compile(r"/data"))

    response = JsonSession().get("https://h/data")
    assert isinstance(response, JsonResponse)


def test_session_uses_custom_json_decoder(httpretty):
    httpretty.register_uri(
        httpretty.GET,
        re.compile(r"/data"),
        serialize({"datetime": datetime(2021, 12, 4)}),
    )

    response = JsonSession().get("https://h/data")
    data = response.json()
    assert isinstance(data["datetime"], datetime)


def test_session_uses_custom_json_encoder(httpretty):
    httpretty.register_uri(httpretty.GET, re.compile(r"/data"))

    response = JsonSession().get(
        "https://h/data", json={"dt": datetime(2021, 12, 4)}
    )

    assert response.request.body == b'{"dt": "2021-12-04T00:00:00"}'


class CustomResponse(JsonResponse):
    pass


class ReplaceDefaultsSession(JsonSession):
    JSON_ENCODER = json.JSONEncoder
    JSON_DECODER = json.JSONDecoder
    RESPONSE_CLASS = CustomResponse


def test_session_subclass_uses_custom_response_subclass(httpretty):
    httpretty.register_uri(httpretty.GET, re.compile(r"/data"))

    response = ReplaceDefaultsSession().get("https://h/data")
    assert isinstance(response, CustomResponse)


def test_session_subclass_with_another_decoder(httpretty):
    httpretty.register_uri(
        httpretty.GET,
        re.compile(r"/data"),
        serialize({"datetime": datetime(2021, 12, 4)}),
    )

    response = ReplaceDefaultsSession().get("https://h/data")
    data = response.json()
    assert isinstance(data["datetime"], str)


def test_session_subclass_with_another_encoder(httpretty):
    httpretty.register_uri(httpretty.GET, re.compile(r"/data"))

    with pytest.raises(TypeError):
        ReplaceDefaultsSession().get(
            "https://h/data", json={"dt": datetime(2021, 12, 4)}
        )
