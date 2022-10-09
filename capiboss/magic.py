import functools
import gc
import inspect
from types import FunctionType
from typing import Union, get_origin, get_type_hints

from cattr import Converter

DEFAULT_CONVERTER = Converter()


class CallersHintedArgs:
    @staticmethod
    def get_caller_and_locals(previous=0):
        """Previous defines how far back on the stack we go.
        0 is the current frame (inside this function).
        1 is the caller.
        2 and on get's the callers before.
        """
        try:
            # Get the propper frame.
            frame = inspect.currentframe()
            for _ in range(previous):
                frame = frame.f_back

            localns = frame.f_locals
            fcode = frame.f_code

            # Searches for the first reference to the related code object.
            function = next(f for f in gc.get_referrers(fcode) if isinstance(f, FunctionType))
        finally:
            del frame

        return function, localns

    @staticmethod
    def hints(function, localns):
        hints = get_type_hints(function, localns=localns)
        rtype = hints.pop("return", None)
        return hints, rtype

    @staticmethod
    def filter_args(localns, hints):
        is_undefined = lambda value, t: get_origin(t) is Union and value is None  # noqa E731

        return {k: localns[k] for k, t in hints.items() if not is_undefined(localns[k], t)}

    @classmethod
    def informed(cls, previous=2):
        """This function should be called by the service method."""
        function, localns = cls.get_caller_and_locals(previous=previous)
        arg_hints, rtype = cls.hints(function, localns)
        return cls.filter_args(localns, arg_hints)


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
