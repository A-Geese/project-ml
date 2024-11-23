import os

from tinydb import TinyDB


def get_db(db_path: str) -> TinyDB:
    """Creates db if does not exist else returns the db"""

    if not db_path:
        raise ValueError("No db path provided")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    db = TinyDB(db_path)

    return db


def write():
    pass


def update():
    pass


def read():
    pass
