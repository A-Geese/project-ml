import os

from tinydb import Query, TinyDB


def get_db(db_path: str) -> TinyDB:
    """Creates db if does not exist else returns the db"""

    if not db_path:
        raise ValueError("No db path provided")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    db = TinyDB(db_path)

    return db


def get_agent_with_name(db: TinyDB, name: str) -> dict:
    User = Query()
    name = name.lower()
    res = db.search(User.name == name)
    return res[0]
