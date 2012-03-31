import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Point(Base):
    __tablename__ = "point"
    query = DBSession.query_property()
    id = sa.Column(sa.Integer,primary_key=True)
    x = sa.Column(sa.Integer)
    y = sa.Column(sa.Integer)
    name = sa.Column(sa.String(255))

