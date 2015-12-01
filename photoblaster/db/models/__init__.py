from photoblaster.db import SessionHeap
from sqlalchemy import inspect, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func


Base = declarative_base()


class Actions(object):
    @classmethod
    def create(cls, **kwargs):
        session = SessionHeap()
        session.add(cls(**kwargs))
        session.commit()
        session.close()
        SessionHeap.remove()

    def update(self, **kwargs):
        for key, val in kwargs.iteritems():
            self.__setattr__(key, val)
        session = inspect(self).session
        session.commit()

    @classmethod
    def _search(cls, **kwargs):
        session = SessionHeap()
        query = session.query(cls).filter_by(**kwargs)
        SessionHeap.remove()
        return query

    @classmethod
    def search_random(cls, **kwargs):
        return cls._search(**kwargs).order_by(func.rand())

    @classmethod
    def search(cls, **kwargs):
        return cls._search(**kwargs).order_by(desc(cls.id))

    @classmethod
    def query(cls, **kwargs):
        session = SessionHeap()
        query = session.query(cls)
        SessionHeap.remove()
        return query
