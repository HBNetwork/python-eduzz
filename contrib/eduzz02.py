from pprint import pprint

from decouple import config

from eduzz.core import Eduzz

client = Eduzz.from_credentials(
    email=config("EDUZZ_EMAIL"),
    publickey=config("EDUZZ_PUBLICKEY"),
    apikey=config("EDUZZ_APIKEY"),
)

g = client.get_sales_list("2021-11-01", "2021-11-30")

data = list(g)

pprint(len(data))
