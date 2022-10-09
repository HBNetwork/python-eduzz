from requests_futures.sessions import FuturesSession


def response_for_urls(urls):
    """Asynchronously get response for many urls."""
    with FuturesSession() as session:
        futures = [session.get(url) for url in urls]

    return (f.result() for f in futures)


if __name__ == "__main__":
    urls = [
        "https://www.google.com",
        "https://www.discourse.org",
        "https://www.stackoverflow.com",
        "https://www.henriquebastos.net",
    ]

    print(list(response_for_urls(urls)))
