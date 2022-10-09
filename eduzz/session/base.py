import requests


class BaseSession(requests.Session):
    def __init__(self, **kwargs):
        super(BaseSession, self).__init__()
