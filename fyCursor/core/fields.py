from typing import Optional, Any
from ..constants.sql_types import DATATYPES


def _pass() -> str:
    return ''


class Field():
    def __init__(
        self,
        name: Optional[str] = None,
        default: Any = None,
        nullable: bool = True,
        primary_key: bool = False,
        type: str = DATATYPES.TEXT
    ) -> None:
        self.name = name
        self.primary_key = primary_key
        self.default = default
        self.nullable = nullable
        self.type = type

    def _generate_field(self) -> str:
        self._field = self.name or ''
        self._field += self.type
        self._field += " PRIMARY KEY" if self.primary_key else _pass()
        self._field += (
            f"DEFAULT \"{self.default}\"" if self.default else _pass()
        )
        self._field += _pass() if self.nullable else " NOT NULL"

        return self._field
