"""Export sales."""

from decouple import config

from eduzz.core import Eduzz

client = Eduzz.from_credentials(
    email=config("EDUZZ_EMAIL"),
    publickey=config("EDUZZ_PUBLICKEY"),
    apikey=config("EDUZZ_APIKEY"),
)

with open("./api-records/sale-get_sale_list.json", "w") as f:
    for r in client.get_sales_list("2021-11-01", "2021-11-30"):
        f.write(f"// {r.url}\n")
        f.write(r.text)
        f.write("\n\n")
