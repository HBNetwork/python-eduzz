from datetime import date
from functools import wraps, update_wrapper
from inspect import Signature, isfunction, _empty as EMPTY
from typing import Optional, List

import pytest
from attr import define

from eduzz.converters import converter


class SignatureWithParams(Signature):
    PARAMS = "params"

    def __init__(
        self,
        parameters=None,
        *,
        return_annotation=Signature.empty,
        __validate_parameters__=True,
    ):
        super().__init__(parameters, return_annotation=return_annotation)

    @staticmethod
    def has_hint(param):
        return param.annotation is not param.empty

    @property
    def params(self):
        return self.parameters.get(self.PARAMS, self.empty)

    def hinted(self):
        """Returns a list of params with type hints."""
        return [
            p
            for p in self.parameters.values()
            if self.has_hint(p) and p is not self.params
        ]

    def bind_hinted(self, *args, **kwargs):
        hinted_sig = Signature(
            parameters=self.hinted(), return_annotation=self.return_annotation
        )
        binded_args = hinted_sig.bind_partial(*args, **kwargs)
        binded_args.apply_defaults()
        return binded_args


class hintconvert:
    CONVERTER = converter

    def __init__(self, func):
        self.func = func
        self.signature = SignatureWithParams.from_callable(func)
        update_wrapper(self, func)

    def bind_to_hints(self, *args, **kwargs):
        ba = self.signature.bind_hinted(*args, **kwargs)
        return ba.arguments, ba.signature.return_annotation

    @staticmethod
    def convert(data, type_):
        if type_ is EMPTY:
            return data
        return converter.structure(data, type_)

    def __call__(self, *args, **kwargs):
        arguments, rtype = self.bind_to_hints(*args, **kwargs)
        r = self.func(*args, params=arguments, **kwargs)
        return self.convert(r, rtype)


def method_decorator(decorator):
    """
    Converts a function decorator into a method decorator.
    """

    def _dec(func):
        def _wrapper(self, *args, **kwargs):
            @wraps(func)
            def bound_func(*args2, **kwargs2):
                return func(self, *args2, **kwargs2)

            # bound_func has the signature that 'decorator' expects i.e.  no
            # 'self' argument, but it is a closure over self so it can call
            # 'func' correctly.
            return decorator(bound_func)(*args, **kwargs)

        return wraps(func)(_wrapper)

    update_wrapper(_dec, decorator)
    # Change the name, to avoid confusion, as this is *not* the same
    # decorator.
    _dec.__name__ = f"method_dec({decorator.__name__})"
    return _dec


def autoconvert(cls):
    dec_for_method = method_decorator(hintconvert)
    for k, v in cls.__dict__.items():
        if isfunction(v):
            setattr(cls, k, dec_for_method(v))

    return cls


@define
class Sale:
    product: str
    qty: int
    value: float


@pytest.fixture
def f():
    def fn(
        start_date: date,
        end_date: date,
        page: Optional[int] = None,
        client_email: Optional[str] = None,
        parallel=True,
        params=None,
    ) -> List[Sale]:
        return [
            {"product": "ProductA", "qty": 1, "value": 1.99},
            {"product": "ProductB", "qty": 2, "value": 4.20},
        ]

    return fn


@pytest.fixture
def g():
    def fn(
        start_date: date,
        end_date: date,
        page: Optional[int] = None,
        client_email: Optional[str] = None,
        parallel=True,
        params=None,
    ):
        return [
            {"product": "ProductA", "qty": 1, "value": 1.99},
            {"product": "ProductB", "qty": 2, "value": 4.20},
        ]

    return fn


def test_custom_signature_state(f):
    cs = SignatureWithParams.from_callable(f)

    assert len(cs.parameters.keys()) == 6
    assert len(cs.hinted()) == 4
    assert len([p for p in cs.parameters.values() if p is cs.params]) == 1
    assert len([p for p in cs.hinted() if p is cs.params]) == 0
    assert cs.params is not SignatureWithParams.empty


def test_custom_signature_bind(f):
    cs = SignatureWithParams.from_callable(f)

    ba = cs.bind_hinted(1, end_date=2, page=3)

    assert {
        "start_date": 1,
        "end_date": 2,
        "page": 3,
        "client_email": None,
    } == ba.arguments


def test_custom_signature_bind_pargs_as_kwargs():
    def f(self, start_date: date, params=None) -> Sale:
        return Sale()

    cs = SignatureWithParams.from_callable(f)

    ba = cs.bind_hinted(*(), start_date=1)

    assert {
        "start_date": 1,
    } == ba.arguments


def test_decorator_do_convert(f):
    decorated = hintconvert(f)

    l = decorated(1, end_date=2, page=3)
    assert isinstance(l, list)
    assert all(isinstance(e, Sale) for e in l)


def test_decorator_do_not_convert(g):
    decorated = hintconvert(g)

    l = decorated(1, end_date=2, page=3)
    assert isinstance(l, list)
    assert all(isinstance(e, dict) for e in l)


def test_class_decorated():
    @autoconvert
    class C:
        def a(self, params=None):
            return {"a": 1, "b": 2}

        def b(self, start_date: str, params=None) -> Sale:
            return {"product": "ProductA", "qty": 1, "value": 1.99}

    assert C().a() == {"a": 1, "b": 2}

    assert C().b(start_date="date") == Sale(
        product="ProductA", qty=1, value=1.99
    )

    assert C().b("date") == Sale(
        product="ProductA", qty=1, value=1.99
    )


if __name__ == "__main__":
    ...
    # pytest.main(["-s", __main__])
