from eduzz.magic import CallersHintedArgs


class BaseService:
    def __init__(self, client):
        self.client = client

    def params(self):
        return CallersHintedArgs.informed(previous=3)
