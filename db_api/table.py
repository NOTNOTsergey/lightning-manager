from db_api import SqlAlchemyBase
import sqlalchemy as sql
from sqlalchemy import Column as Cl
from sqlalchemy import orm



class Password(SqlAlchemyBase):
    __tablename__ = "passwords"

    id = Cl(sql.Integer, autoincrement=True, unique=True, nullable=False, primary_key=True)
    password = Cl(sql.String, nullable=False)
    name = Cl(sql.String, nullable=False)
    description = Cl(sql.String, nullable=False)