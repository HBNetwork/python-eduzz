import re

from responses import RequestsMock as OriginalRequestsMock


class RequestsMock(OriginalRequestsMock):
    @staticmethod
    def is_relative(url, first="/"):
        return url and url.startswith(first)

    @staticmethod
    def regex_for_path(path):
        """Build a regex to match any host ending in path."""
        host = r".+"
        return re.compile(host + path)

    def add(self, method=None, url=None, *args, **kwargs):
        if isinstance(url, str) and self.is_relative(url):
            url = self.regex_for_path(url)

        return super().add(method=method, url=url, *args, **kwargs)
