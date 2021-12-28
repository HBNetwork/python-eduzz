from concurrent.futures import Future
from itertools import chain

import requests
from requests_futures.sessions import FuturesSession
from urlobject import URLObject as Url


class Paginator:
    def __init__(self, url, page=1, totalPages=1):
        self.url = Url(url)
        self.page = page
        self.totalPages = totalPages

    def __len__(self):
        return self.totalPages

    def _url_for_index(self, index):
        return str(self.url.set_query_param("page", index + 1))

    def __getitem__(self, item):
        if isinstance(item, slice):
            return [
                self._url_for_index(index)
                for index in range(*item.indices(len(self)))
            ]
        else:
            index = item if item >= 0 else len(self) + item

            if index < 0 or index >= self.totalPages:
                raise IndexError("Index out of range.")
            return self._url_for_index(index)

    def update(self, totalPages=None, **kwargs):
        self.totalPages = totalPages or self.totalPages


class PaginatedSession(requests.Session):
    @staticmethod
    def pagination(r):
        return r.json()["paginator"]

    def get_all(self, url, parallel=False, **kwargs):
        if parallel:
            yield from self.get_in_paralel(url, **kwargs)
        else:
            yield from self.get_on_demand(url, **kwargs)

    def get_on_demand(self, url, **kwargs):
        paginator = Paginator(url)

        for next_url in paginator:
            r = self.get(next_url, **kwargs)
            yield r
            paginator.update(**self.pagination(r))

    def get_in_paralel(self, url, **kwargs):
        paginator = Paginator(url)
        next_url = paginator[0]
        r = self.get(next_url, **kwargs)
        r.raise_for_status()

        paginator.update(**self.pagination(r))

        with FuturesSession(session=self) as session:
            futures = [
                session.get(next_url, **kwargs) for next_url in paginator[1:]
            ]

        first = Future()
        first.set_result(r)

        for future in chain((first,), futures):
            yield future.result()
