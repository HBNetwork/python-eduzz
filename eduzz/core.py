from eduzz.auth import EduzzToken
from eduzz.sessions import EduzzSession


class Eduzz:
    def __init__(self, session):
        self.session = session

    @classmethod
    def from_credentials(cls, **credentials):
        auth = EduzzToken(**credentials)
        session = EduzzSession()
        session.auth = auth

        return cls(session)

    def get_sales_list(self, start_date, end_date):
        next_page = 1
        params = {"start_date": start_date, "end_date": end_date, "page": next_page}

        response = self.session.get("/sale/get_sale_list", params=params)
        response.raise_for_status()
        json = response.json()

        data = json["data"]
        paginator = json["paginator"]  # noqa
        profile = json["profile"]
        token = profile["token"]  # noqa
        token_valid_until = profile["token_valid_until"]  # noqa

        yield from data
        #
        # next_page = paginator['page'] + 1
        # params['page'] = next_page
        #
        # response = requests.get(URL.add_path('/sale/get_sale_list'), headers=headers, params=params)
        #
        # json = response.json(cls=JSONDecoder)
        #
        # data = json['data']
        # paginator = json['paginator']
        # profile = json['profile']
        # token = profile['token']
        # token_valid_until = profile['token_valid_until']
        # headers['token'] = token
        #
        # yield from data
