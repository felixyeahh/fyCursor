import sqlite3 as _sq3
from fyCursor.core import fyCursor

def connect(
    database: str, 
) -> 'fyCursor':

    connection = _sq3.connect(
        database=database, 
    )
    return connection.cursor(fyCursor) #type: ignore


__title__ = "fyCursor"

__version__  = "0.0.3"

__author__ = "felixyeahh"
__author_email__ = "<felixyeah@outlook.com>"

__license__ = "MIT"
__copyright__ = "Copyright 2023 Baffu"

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
    "connect", "fyCursor", "__title__", 
    "__version__", "__author__", "__author_email__", 
    "__license__", "__copyright__", "__description__", 
    "Info"
]
