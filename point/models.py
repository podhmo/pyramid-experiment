import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

class MyBaseMeta(object):
    def as_dict(self):
        from sqlalchemy.sql.operators import ColumnOperators
        return {k: getattr(self, k) for k, v in self.__class__.__dict__.iteritems() \
                    if isinstance(v, ColumnOperators)}
    @classmethod
    def from_dict(cls, D):
        instance = cls()
        items_fn = D.iteritems if hasattr(D, "iteritems") else D.items
        for k, v in items_fn():
            setattr(instance, k, v)
        return instance

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base(cls=MyBaseMeta)

class Point(Base):
    __tablename__ = "point"
    query = DBSession.query_property()
    id = sa.Column(sa.Integer,primary_key=True)
    x = sa.Column(sa.Integer)
    y = sa.Column(sa.Integer)
    name = sa.Column(sa.String(255))


