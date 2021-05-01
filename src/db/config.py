import os
from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# region Database locale
session_factory: sessionmaker = sessionmaker(create_engine(
    os.environ.get('SQLALCHEMY_DATABASE_URI'),
    connect_args={'connect_timeout': 1000}), expire_on_commit=False)


def get_session() -> sessionmaker:
    return session_factory
# endregion