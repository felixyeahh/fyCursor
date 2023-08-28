# pyright: reportPrivateUsage=false
import logging

from sqlite3 import Cursor, Connection, ProgrammingError

from .fields import Field
from typing import Union, Any, Optional, Self


NULL = None


class TableError(BaseException):
    """Raised if something went wrong while creating a table class"""


class TableInsert():
    def __init__(
        self,
        table: "Table",
        *args: str
    ) -> None:
        self.table = table
        self.args = args


class Table():
    def __init__(
        self,
        name: str,
        cursor: "fyCursor",
        args_fields: Optional[list[Field]] = None,
        kwargs_fields: Optional[dict[str, Field]] = None
    ) -> None:
        assert kwargs_fields or args_fields, (
            "you should provide either args_fields or kwargs_fields"
        )
        self._table: list[str] = []
        self._sql = ""
        self.name = name
        self.cursor = cursor
        if kwargs_fields is not None:
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
            return f"\"{name}\","

        names = ""
        for item in names_:
            names += generate_name(item)

        values = ""
        for item in values_:
            values += generate_name(item)

        self.cursor.execute(
            f"INSERT INTO {self.name}({names[:-1]}) VALUES ({values[:-1]})"
        ).commit()

        return self

    def __lshift__(self, __b: dict[str, Any]) -> "Table":
        """Insert dict using left shift (<<) operator"""
        if not isinstance(__b, dict):  # type: ignore
            raise TableError("Wrong arguments")
        self.insert(**__b)
        return self

    def delete(self, **kwargs: Any) -> "Table":
        """
            Same as `DELETE FROM {table.name} WHERE kwargs.keys=kwargs.values`
        """
        names_ = list(kwargs.keys())
        values_ = list(kwargs.values())

        where = str()
        is_first = True
        for name, value in zip(names_, values_):
            if not is_first:
                where += "AND"
            where += f"{name} = \"{value}\""
            is_first = False

        self.cursor.execute(f"DELETE FROM {self.name} WHERE {where}").commit()
        return self

    def __rshift__(self, __b: dict[str, Any]) -> "Table":
        """Delete dict using right shift (>>) operator"""
        if not isinstance(__b, dict):  # type: ignore
            raise TableError("Wrong arguments")
        self.delete(**__b)
        return self

    def get_values(self) -> dict[str, Field]:
        return self._fields

    def create(self, if_not_exist: bool = False) -> "Table":
        return self.cursor.create_table(self, if_not_exist)


class fyCursor(Cursor):
    """
    Custom `sqlite3.Cursor` that can be used without string query. \n
    I just hate query because it does not have any highlighting in IDE, yeah.

    https://github.com/felixyeahh/fyCursor
    """
    def __init__(
        self,
        __cursor: Connection,
        logger: Any = None
    ) -> None:
        """
        Initialise a cursor.

        :param __cursor - sqlite3 connection
        :param logger - custom logger (Optional)
        """
        self.null = NULL
        self.NULL = self.null
        # setting null constant so user will be able to easily access it

        self._empty_query()  # set query to None

        super().__init__(__cursor)

        self._logger = logging.getLogger(
            "fyCursor"
        ) if logger is None else logger

    def set_logger(self, logger: Any) -> Self:
        """
        Sets a custom logger. Logger class should have following methods: \
            info, warning, exception

        :param logger: - logger
        :returns: - self
        """
        self._logger = logger

        return self

    def _empty_query(self) -> None:
        self._execution = self._query = None

    def check_method(self, *methods: str) -> bool:
        """
        Checks if provided methods are qurrently in query

        :*methods: - str name of methods
        :returns: - bool
        """
        if len(methods) > 1:
            return False not in [self.check_method(method)
                                 for method in methods]
        elif not methods:
            return True
        elif self._query is None:
            return False
        return methods[1] in self._query

    def update(self, table: str) -> Self:
        """
        Use this as SQL `UPDATE {table}` method

        :param table: - table to be updated
        :returns: - self
        """
        self._query = f"UPDATE {table}"

        return self

    def add(self, **kwargs: Any) -> Self:
        """
        Use this as SQL `SET {kwargs.keys}={kwargs.keys}+{kwargs.values}`

        **kwargs

        :returns: - self

        :raises: - `sqlite3.ProgrammingError` if you didn't use
        `fyCursor.update()` or something similar before this statement
        """
        if not self._query:
            raise ProgrammingError(
                "You should use something before `add`"
            )
        column = list(kwargs.keys())[0]
        value = list(kwargs.values())[0]
        self._query += f" SET {column} = {column} + {value}"
        return self

    def set(self, fix: bool = True, **kwargs: Any) -> Self:
        """
        Use this as SQL`SET {kwargs.keys} = {kwargs.values}`

        :returns: - self

        :raises: - `sqlite3.ProgrammingError` if you didn't use
        `fyCursor.update()` or something similar before this statement
        """
        if not self._query:
            raise ProgrammingError(
                "You should use something before `set`"
            )

        column = list(kwargs.keys())[0]
        value = str(list(kwargs.values())[0])
        column = column or "NULL"

        if fix:
            value = f"\"{value}\""

        self._query += f" SET {column} = {value}"
        return self

    def select(self, value: str, from_: Optional[str] = None) -> Self:
        """
        Use this as SQL `SELECT {value} FROM {from_}`

        :param value: - value to be selected
        :param from_: - table from which value will be selected

        :returns: - self
        """
        self._query = f"SELECT {value}"
        if from_ is not None:
            self._from(from_)
        return self

    def _from(self, table: str) -> Self:
        self._query += f" FROM {table}"  # type: ignore
        return self

    def where(self, **kwargs: Any) -> Self:
        if not self._query:
            raise ProgrammingError(
                "You should use something before `where`"
            )
        self._query += (
            f" WHERE {list(kwargs.keys())[0]} "
            f"= \"{list(kwargs.values())[0]}\""
        )
        return self

    def execute(
        self,
        __sql: str,
        *__parameters: Any
    ) -> Self:
        if __parameters:
            for param in __parameters:
                __sql = __sql.replace("?", str(param), 1)
        self._execution = __sql
        return self

    def exec(self, __sql: Any, __parameters: Any = ()):
        """
        Execute using super().execute

        Use if bugs appered in fyCursor.execute
        """
        return super().execute(__sql, __parameters)

    def fetch(
        self,
        one: bool = False
    ) -> Optional[Union[tuple[Any], list[Any]] | Any]:
        """
        fetch values from cursor query

        :param one - if `True` provided, the `cursor.fetchone()`
        function will be used
        """
        if not self._query and not self._execution:
            raise ProgrammingError("Nothing to fetch")

        super().execute(self._query or self._execution)  # type: ignore
        super().connection.commit()

        self._empty_query()

        return super().fetchone() if one else super().fetchall()

    def one(self) -> Any:
        """
        returns exact one result of fetching, not tuple
        """
        fetching = self.fetch(True)

        if fetching is None:
            return None
        elif isinstance(fetching, (list, tuple)):
            return fetching[0]
        return fetching

    def commit(self) -> Self:
        if self._execution:
            print(self._execution)
            super().execute(self._execution)
        elif self._query:
            super().execute(self._query)
        super().connection.commit()

        self._empty_query()

        return self

    def create_table(
        self,
        table: Table,
        if_not_exist: bool = False
    ) -> "Table":
        exist = "IF NOT EXISTS" if if_not_exist else ""
        super().execute(f"""
            CREATE TABLE {exist}\
             {table.name}({table._sql[:-1]})
        """)
        super().connection.commit()

        return table

    def insert_into(self, insert: "TableInsert", *values: Any) -> Table:
        def _prepare(args: tuple[Any]) -> str:
            values = str()
            for arg in args:
                values += f"{arg} ,"
            values = values[:-1]
            return values

        fields = _prepare(insert.args)
        values_ = _prepare(values)

        super().execute(f"""
            INSERT INTO TABLE {insert.table.name} ({fields})
            VALUES ({values_})
        """)
        super().connection.commit()

        return insert.table
