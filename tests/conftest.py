import pytest

from tests.conftools.responses import RequestsMock


@pytest.fixture
def httpretty(allow_net_connect=False, verbose=False):
    import httpretty

    httpretty.reset()
    httpretty.enable(allow_net_connect=allow_net_connect, verbose=verbose)

    yield httpretty

    httpretty.disable()
    httpretty.reset()


@pytest.fixture
def responses(monkeypatch):
    from functools import partial

    import responses as responses_module

    from eduzz.sessions.json_session import BetterJSONDecoder, BetterJSONEncoder

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
