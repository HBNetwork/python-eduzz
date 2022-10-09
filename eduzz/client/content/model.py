from attr import define


@define
class Category:
    category_id: int
    category_name: str
    parent_category_id: int
