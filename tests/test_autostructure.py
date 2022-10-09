from datetime import datetime

from attr import define
from cattr import Converter

from capiboss.magic import autostructure


def converter_with_datetime():
    converter = Converter()
    converter.register_unstructure_hook(datetime, lambda dt: dt.isoformat())
    converter.register_structure_hook(
        datetime,
        lambda s, _: datetime.fromisoformat(s) if isinstance(s, str) else s,
    )
    return converter


@define
class MyModel:
    start_date: datetime
    quantity: int
    description: str


class TestClass:
    @autostructure(converter=converter_with_datetime())
    def get_model(self, **kwargs) -> MyModel:
        return kwargs

    @autostructure
    def get_something(self, arg) -> list[int]:
        return arg

    @autostructure
    def get_by_generator(self, arg) -> list[int]:
        yield from arg


def test_custom_converter():
    assert TestClass().get_model(start_date="2022-09-14", quantity="42", description="Awesome") == MyModel(
        datetime(2022, 9, 14), quantity=42, description="Awesome"
    )


def test_method_pass_through():
    assert TestClass().get_something([1, 2, 3]) == [1, 2, 3]


def test_generator_pass_through():
    assert list(TestClass().get_by_generator([1, 2, 3])) == [1, 2, 3]


def test_method_raise_return_type_mismatch():
    try:
        TestClass().get_something("a b c".split())
    except ValueError:
        pass


def test_generator_raise_return_type_mismatch():
    try:
        list(TestClass().get_by_generator("a b c".split()))
    except ValueError:
        pass
