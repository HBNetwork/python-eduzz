from eduzz.sessions import BaseUrlSession


def test_baseurl():
    s = BaseUrlSession(base_url="https://host")

    assert s.ensure_absolute_url("/data") == "https://host/data"
    assert s.ensure_absolute_url("https://other/data") == "https://other/data"
    assert s.ensure_absolute_url("//other/data") == "//other/data"
