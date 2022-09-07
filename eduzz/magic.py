import functools
from typing import get_type_hints

from cattr import Converter

DEFAULT_CONVERTER = Converter()


def autostructure(f=None, *, converter=DEFAULT_CONVERTER):
    def intermediary(func):
        hints = get_type_hints(func)
        rtype = hints.get("return")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if rtype is not None:
                result = converter.structure(result, rtype)
            return result

        return wrapper

    return intermediary(f) if f else intermediary
