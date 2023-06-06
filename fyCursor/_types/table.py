from ..core.fields import Field
from ..core.cursor import fyCursor
from typing import Any


class TableError(BaseException):
    """Raised if something went wrong while creating a table class"""


class Table():
    def __init__(
        self,
        name: str,
        cursor: fyCursor,
        args_fields: list[Field],
        kwargs_fields: dict[str, Field]
    ) -> None:
        self._table = []
        self._sql = ""
        self.name = name
        self.cursor = cursor
        self._table.extend(
            f"{value} {value_._generate_field()},"
            for value, value_ in kwargs_fields.items()
        )

        for value, value_ in kwargs_fields.items():
            self._sql += f"{value} {value_._generate_field()},"
        if args_fields is not None:
            self._fields = {
                str(arg.name): arg for arg in args_fields
            }
        else:
            return
        for value in args_fields:
            if not value.name:
                del self._table
                del self._fields

                raise TableError(
                    "You must provide name of field if you providing it as "
                    "args to a table."
                )
            self._sql += value._generate_field()
            self._table.append(value._generate_field())

    def insert(self, **kwargs: Any) -> "Table":
        names_ = list(kwargs.keys())
        values_ = list(kwargs.values())

        def generate_name(name: str):
            return f"{name},"

        names = ""
        for item in names_:
            names += generate_name(item)

        values = ""
        for item in values_:
            values += generate_name(item)

        self.cursor.execute(
            f"INSERT INTO {self.name}({names[:-1]}) VALUES ({values[:-1]})"
        )

        return self

    def get_values(self) -> dict[str, Field]:
        return self._fields

    def create(self, if_not_exist: bool = False):
        return self.cursor.create_table(self, if_not_exist)  # type: ignore
