from datetime import datetime

from cattr import Converter

from money import Money

converter = Converter()

converter.register_unstructure_hook(datetime, lambda dt: dt.isoformat())
converter.register_structure_hook(
    datetime,
    lambda s, _: datetime.fromisoformat(s) if isinstance(s, str) else s,
)

converter.register_unstructure_hook(Money, lambda m: str(m))
converter.register_structure_hook(Money, lambda s, _: Money(0 if s is None else s))
