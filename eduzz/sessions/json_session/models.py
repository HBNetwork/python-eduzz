from functools import cache

import requests


class JsonResponse(requests.Response):
    """
    This class is a proper Response subclass that contemplates the API's design decisions.
    This could be an adapter, but we would hit __getattr__ everytime.
    """

    def __init__(self):
        self.json_decoder = None
        super(JsonResponse, self).__init__()

    @classmethod
    def cast(cls, r, json_decoder=None):
        """Smelly magic to circunvent requests coupling to it's own Response class."""
        r.__class__ = cls
        r.json_decoder = json_decoder
        return r

    @cache
    def json(self, **kwargs):
        kwargs.setdefault("cls", self.json_decoder)
        return super(JsonResponse, self).json(**kwargs)
