import argparse
import csv
import locale
import logging
from datetime import date

from attr import asdict
from decouple import config

from eduzz.core import Eduzz


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("start_date", type=date.fromisoformat)
    parser.add_argument("end_date", type=date.fromisoformat)
    parser.add_argument("output", type=argparse.FileType("w"), default="-")
    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    return parser.parse_args()


def verbose():
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def main():
    args = parse_args()

    if args.verbose:
        verbose()

    # Detect process locale.
    locale.setlocale(locale.LC_ALL, "")

    client = Eduzz.from_credentials(
        email=config("EDUZZ_EMAIL"),
        publickey=config("EDUZZ_PUBLICKEY"),
        apikey=config("EDUZZ_APIKEY"),
    )

    it = client.get_sales_list(args.start_date, args.end_date, parallel=False)

    first_sale = next(it)
    first_row = asdict(first_sale)
    headers = first_row.keys()

    writer = csv.DictWriter(args.output, fieldnames=headers)
    writer.writeheader()
    writer.writerow(first_row)
    writer.writerows(asdict(s) for s in it)


if __name__ == "__main__":
    main()
