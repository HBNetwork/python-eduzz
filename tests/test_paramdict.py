from datetime import date

from capiboss.magic import CallersHintedArgs


class A:
    """Fixture class for tests."""

    def method(self, a=1, b=2):
        return CallersHintedArgs.get_caller_and_locals(previous=1)

    @staticmethod
    def static(a=1, b=2):
        return CallersHintedArgs.get_caller_and_locals(previous=1)

    @classmethod
    def clsmethod(cls, a=1, b=2):
        return CallersHintedArgs.get_caller_and_locals(previous=1)


class TestGetCallerAndLocals:
    def test_on_functions(self):
        def f(a=1, b=2):
            return CallersHintedArgs.get_caller_and_locals(previous=1)

        assert f() == (f, dict(a=1, b=2))

    def test_on_methods(self):
        instance = A()
        function = instance.method.__func__
        assert instance.method() == (function, dict(a=1, b=2, self=instance))

    def test_on_staticmethods(self):
        function = A.static
        assert A.static() == (function, dict(a=1, b=2))

    def test_on_classmethods(self):
        function = A.clsmethod.__func__
        assert A.clsmethod() == (function, dict(cls=A, a=1, b=2))


def test_callers_params_as_dict():
    def caller(
        start_date: date,
        end_date: date,
        page: int | None = None,
        contract_id: int | None = None,
        affiliate_id: int | None = None,
        content_id: int | None = None,
        invoice_status: str | None = None,
        client_email: str | None = None,
        date_type: str | None = None,
        parallel=True,
        kwargs: dict = None,
    ) -> dict:
        return CallersHintedArgs.informed()

    assert caller(start_date=1, end_date=2, page=3) == dict(start_date=1, end_date=2, page=3)
