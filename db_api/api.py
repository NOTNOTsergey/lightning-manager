from typing import Optional, List, Callable, Any

from db_api.table import Password
from sqlalchemy.orm import Session
from db_api import SqlAlchemyBase
import os


def create_password(session: Session,
                password: str,
                name: str, 
                description: str) -> Password:
    passwd = Password(password=password, name=name, description=description)
    session.add(passwd)
    return passwd


def remove(session: Session,
           cls: SqlAlchemyBase,
           id_: int) -> None:
    """
    Remove object from database
    :param session: session you want to delete object from, Session
    :param cls: type of object, SqlAlchemyBAse
    :param id_: id of object, int
    :return:
    """
    obj = session.query(cls).get(id_)
    session.delete(obj)


def get_all(session: Session,
            cls: SqlAlchemyBase):
    """
    Get all objects of cls type from database
    :param session: session you want to get objects from
    :param cls: type of objects you want to get
    :return:
    """

    return session.query(cls).all()
