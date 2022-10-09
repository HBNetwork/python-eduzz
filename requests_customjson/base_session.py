from requests import Session


class BaseSession(Session):
    """A base class for resquests.Session that accepts kwargs to ease complex inheritance hierarchyes."""

    def __init__(self, **kwargs):
        super(BaseSession, self).__init__()
