from decimal import ROUND_HALF_UP, Decimal


class Money(Decimal):
    def __new__(cls, value=0, decimal_precision=2):
        number = super().__new__(cls, value)
        if not number._is_precise(decimal_precision):
            number = number._round(decimal_precision)
        return number

    def __repr__(self):
        return "{0}({1!r})".format(self.__class__.__name__, super().__str__())

    def __str__(self):
        return "{:n}".format(self)

    def _is_precise(self, precision):
        return abs(self.as_tuple().exponent) == precision

    def _round(self, decimal_precision=2):
        number = self.quantize(Decimal(str(1 / 10**decimal_precision)), rounding=ROUND_HALF_UP)
        return Money(number, decimal_precision)


def test_money():
    assert Money(".00") == 0
    assert str(Money(".00")) == "0.00"

    assert Money("1.2345") == Money("1.23")
    assert type(Money("1.23")) is Money
    assert repr(Money("1.23")) == "Money('1.23')"

    assert str(Money("33.99")) == "33.99"
    assert str(Money("-2.66")) == "-2.66"
    assert str(Money("1.1234", decimal_precision=3)) == "1.123"

    import locale

    loc = locale.getlocale()
    locale.setlocale(locale.LC_ALL, "pt_BR")
    assert str(Money("33.99")) == "33,99"
    locale.setlocale(locale.LC_ALL, loc)
