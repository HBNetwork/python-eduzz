from datetime import datetime

from eduzz.sessions import serialize, EduzzSession, EduzzResponse

URL = EduzzSession.ENDPOINT + "/"


def test_session_returns_response_subclass(httpretty):
    httpretty.register_uri(httpretty.GET, URL)

    response = EduzzSession().get("/")
    assert isinstance(response, EduzzResponse)


def test_session_uses_custom_json_decoder(httpretty):
    httpretty.register_uri(
        httpretty.GET, URL, serialize({"datetime": datetime(2021, 12, 4)})
    )

    response = EduzzSession().get("/")
    data = response.json()
    assert isinstance(data["datetime"], datetime)


def test_session_uses_custom_json_encoder(httpretty):
    httpretty.register_uri(httpretty.GET, URL)

    response = EduzzSession().get("/", json={"dt": datetime(2021, 12, 4)})

    assert response.request.body == b'{"dt": "2021-12-04T00:00:00"}'
