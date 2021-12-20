import pytest


@pytest.fixture
def httpretty(allow_net_connect=False, verbose=False):
    import httpretty

    httpretty.reset()
    httpretty.enable(allow_net_connect=allow_net_connect, verbose=verbose)

    yield httpretty

    httpretty.disable()
    httpretty.reset()
