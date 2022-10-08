import re

import pytest

from eduzz.sessions import dumps
from eduzz.sessions.paginator import PaginatedSession, Paginator


def test_paginator():
    url = "https://host/path?a=1&b=2"

    p = Paginator(url, page=1, totalPages=2)
    assert len(p) == 2
    assert p[0] == "https://host/path?a=1&b=2&page=1"
    assert p[1] == "https://host/path?a=1&b=2&page=2"
    with pytest.raises(IndexError):
        p[2]

    assert p[-1] == "https://host/path?a=1&b=2&page=2"

    assert list(p) == [
        "https://host/path?a=1&b=2&page=1",
        "https://host/path?a=1&b=2&page=2",
    ]

    assert p[:1] == ["https://host/path?a=1&b=2&page=1"]
    assert p[1:] == ["https://host/path?a=1&b=2&page=2"]


@pytest.mark.parametrize("parallel", (False, True))
def test_session_returns_all_pages(httpretty, parallel):
    httpretty.register_uri(
        httpretty.GET,
        re.compile(r"/data\?page=1"),
        match_querystring=True,
        body=dumps(
            {
                "data": [{"id": 1}, {"id": 2}],
                "paginator": dict(page=1, size=2, totalPages=2, totalRows=3),
            }
        ),
    )

    httpretty.register_uri(
        httpretty.GET,
        re.compile(r"/data\?page=2"),
        match_querystring=True,
        body=dumps(
            {
                "data": [{"id": 3}],
                "paginator": dict(page=2, size=1, totalPages=2, totalRows=3),
            }
        ),
    )

    responses = list(PaginatedSession().get_all("https://h/data", parallel=parallel))
    assert responses[0].url == "https://h/data?page=1"
    assert responses[1].url == "https://h/data?page=2"

    assert list((d for r in responses for d in r.json()["data"])) == [
        {"id": 1},
        {"id": 2},
        {"id": 3},
    ]

    assert len(httpretty.latest_requests()) == 2
