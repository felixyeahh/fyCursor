import sqlite3 as _sq3
import typing as _typing
import os as _os

from .core import (
    fyCursor,
    Table,
    Field,
    TableError,
    TableInsert,
    NULL
)
from .sql_types import (
    DATATYPES,
    INTEGER,
    TEXT,
    DATETIME,
    VARCHAR,
    BOOL,
    TIMESTAMP
)


def connect(
    database: _os.PathLike[_typing.Any] | str,
) -> 'fyCursor':
    """
    Connect database and return cursor

    Alternative to:
    >>> import sqlite3
    ... from fyCursor import fyCursor
    ... conn = sqlite3.connect("database-name.db")
    ... cur = conn.cursor(fyCursor) # and now you can use this cursor

    :param database - name of the database file
    :returns fyCursor.fyCursor

    """
    connection = _sq3.connect(
        database=database,
    )
    return connection.cursor(fyCursor)  # type: ignore


__title__ = "fyCursor"

__version__ = "0.1.5.1"

__author__ = "felixyeahh"
__author_email__ = "<felixyeah@outlook.com>"

__license__ = "MIT"
__copyright__ = "Copyright 2023 Baffu Team"

__description__ = 'Simple sqlite3 cursor'


class Info():
    __title__ = __title__
    __version__ = __version__
    __author__ = __author__
    __author_email__ = __author_email__
    __license__ = __license__
    __copyright__ = __copyright__
    __description__ = __description__
    __name__ = __name__


__all__ = [
    "connect",
    "fyCursor",
    "Info",
    "Table",
    "Field",
    "TableError",
    "TableInsert",
    "NULL",
    "DATATYPES",
    "INTEGER",
    "TEXT",
    "DATETIME",
    "VARCHAR",
    "BOOL",
    "TIMESTAMP",
    "__title__",
    "__version__",
    "__author__",
    "__author_email__",
    "__license__",
    "__copyright__",
    "__description__"
]
