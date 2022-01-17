from typing import get_type_hints, Union, get_origin


class Service:
    def __init__(self, client):
        self.client = client

    @staticmethod
    def params_filtered(f, data):
        hints = get_type_hints(f, localns=data)
        return {
            k: data[k]
            for k, t in hints.items()
            if not (get_origin(t) is Union and data[k] is None)
        }
