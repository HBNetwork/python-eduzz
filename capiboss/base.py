from capiboss.magic import CallersHintedArgs


class BaseClient:
    def __init__(self, client):
        self.client = client

    def params(self):
        return CallersHintedArgs.informed(previous=3)
