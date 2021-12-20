from datetime import datetime
from re import compile as regex

import pytest
import requests
from freezegun import freeze_time
from responses import RequestsMock

from eduzz.sessions import EduzzAuth, EduzzAPIError, EduzzSession
from eduzz.tests import ResponsesSequence

NOW = datetime(2021, 12, 4, 0, 0, 0)
BEFORE_NOW = datetime(2021, 12, 3, 23, 59, 59)
NOW_PLUS_15 = datetime(2021, 12, 4, 0, 15, 0)


def test_auth_is_expired_on_init(auth):
    assert auth.is_expired


@freeze_time(NOW)
def test_auth_expiration_logic(auth):
    assert auth.is_expired, "Token should be empty."

    auth.token = ("VALID", NOW)
    assert not auth.is_expired, "Token should be valid on the limit."

    auth.token = ("EXPIRED", BEFORE_NOW)
    assert auth.is_expired, "Token should be just expired."


def test_auth_renew_when_token_empty(auth, req, responses):
    responses.add(
        responses.POST,
        regex(".+/generate_token"),
        json=token_body(token="VALID"),
        status=201,
    )

    req.prepare("GET", "https://h/first", auth=auth)

    assert req.headers["Token"] == "VALID"


@freeze_time(NOW)
def test_auth_renew_when_token_expired(auth, req, responses):
    auth.token = ("EXPIRED", BEFORE_NOW)

    responses.add(
        responses.POST,
        regex(".+/generate_token"),
        json=token_body("VALID", NOW_PLUS_15),
        status=201,
    )

    req.prepare("GET", "https://h/first", auth=auth)

    assert req.headers["Token"] == "VALID"


def test_auth_raises_for_empty_credentials(auth, req, responses):
    responses.add(
        responses.POST,
        regex(".+/generate_token"),
        json=error_body("#0001"),
        status=401,
    )

    with pytest.raises(EduzzAPIError, match="#0001 Empty credentials"):
        req.prepare("GET", "https://h/first", auth=auth)


def test_auth_raises_for_invalid_credentials(auth, req, responses):
    responses.add(
        responses.POST,
        regex(".+/generate_token"),
        json=error_body("#0002"),
        status=401,
    )

    with pytest.raises(EduzzAPIError, match="#0002 Invalid credentials"):
        req.prepare("GET", "https://h/first", auth=auth)


def test_auth_raise_for_forbidden_access(auth, req, responses):
    responses.add(
        responses.POST,
        regex(".+/generate_token"),
        json=error_body("#0010"),
        status=401,
    )

    with pytest.raises(EduzzAPIError, match="#0010 Forbiden access"):
        req.prepare("GET", "https://h/first", auth=auth)


@freeze_time(NOW)
def test_auth_recover_from_undetected_expired_token(auth, responses):
    responses.add_callback(
        responses.POST,
        regex(".+/generate_token"),
        ResponsesSequence(
            (201, "", token_body("T1", NOW)),
            (201, "", token_body("T2", NOW_PLUS_15)),
        ),
    )

    responses.add_callback(
        responses.GET,
        "https://h/first",
        ResponsesSequence(
            (401, "", error_body("#0029")), (200, "", data_body())
        ),
    )

    r = requests.get("https://h/first", auth=auth)

    assert len(responses.calls) == 4
    assert r.status_code == 200


@freeze_time(NOW)
def test_auth_updates_with_refreshed_token(auth, responses):
    responses.add(
        responses.POST,
        regex(".+/generate_token"),
        status=201,
        json=token_body("VALID", NOW),
    )

    responses.add(
        responses.GET,
        regex(".+/first"),
        status=200,
        json=data_body(token="T2", token_valid_until=NOW_PLUS_15),
    )

    requests.get("https://h/first", auth=auth)

    assert len(responses.calls) == 2
    assert auth.token == "T2", NOW_PLUS_15


@pytest.fixture
def auth():
    return EduzzAuth("e@mail.com", "PUBLICKEY", "APIKEY", EduzzSession)


@pytest.fixture
def req():
    return requests.PreparedRequest()


@pytest.fixture
def responses(monkeypatch):
    import responses as responses_module
    from functools import partial
    from eduzz.serializers import BetterJSONEncoder, BetterJSONDecoder

    with monkeypatch.context() as m:
        m.setattr(
            responses_module.json_module,
            "loads",
            partial(responses_module.json_module.loads, cls=BetterJSONDecoder),
        )
        m.setattr(
            responses_module.json_module,
            "dumps",
            partial(responses_module.json_module.dumps, cls=BetterJSONEncoder),
        )
        with RequestsMock() as rm:
            yield rm


ERRORS = {
    "#0001": "Empty credentials",
    "#0002": "Invalid credentials",
    "#0010": "Forbiden access",
    "#0029": "Expired Jwt Token",
}


def error_body(code):
    return {
        "success": False,
        "code": code,
        "details": ERRORS[code],
        "link": "https://api2.eduzz.com",
    }


def token_body(token="VALID", token_valid_until=NOW_PLUS_15):
    return {
        "success": True,
        "data": {"token": token, "token_valid_until": token_valid_until},
    }


def data_body(token="VALID", token_valid_until=NOW_PLUS_15):
    return {
        "success": True,
        "data": [{"id": 1}],
        "profile": {"token": token, "token_valid_until": token_valid_until},
    }
