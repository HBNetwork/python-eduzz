from requests.adapters import HTTPAdapter


class JsonAdapter(HTTPAdapter):
    def __init__(self, response_factory, **kwargs):
        self.response_factory = response_factory
        super(JsonAdapter, self).__init__(**kwargs)

    def send(self, *args, **kwargs):
        r = super(JsonAdapter, self).send(*args, **kwargs)
        return self.response_factory(r)
