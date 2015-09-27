# coding: utf-8
"""all database connections and logic goes here"""
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import time, sys

from sqlalchemy import Column, Integer, LargeBinary, String, create_engine, sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
_NULL = sql.null()

Base = declarative_base()
metadata = Base.metadata

class ImCmd(Base):
    """defines the table class"""
    __tablename__ = 'im_cmd'
    id = Column(Integer, primary_key=True)
    date = Column(Integer)
    remote_addr = Column(String(16))
    name = Column(String(16))
    url = Column(String(256))
    dir = Column(String(2))
    oldfile = Column(String(256))
    newfile = Column(String(256))
    cmd = Column(LargeBinary)
    dataobj = Column(LargeBinary)
    tag = Column(String(50))

class Db(object):
    """wrapper for all db methods"""
    def __init__(self):
        engine = create_engine('mysql://{}:{}@{}/{}'.format(
            DB_USER,
            DB_PASSWORD,
            DB_HOST,
            DB_NAME
        ))
        self.Session = sessionmaker(bind=engine)

    def insert_cmd(self, **kwargs):
        try:
            session = self.Session()
            _entry_data = {
                'date' : kwargs.get("date", int(time.time())),
                'remote_addr' : kwargs['remote_addr'] or _NULL,
                'name' : kwargs['username'] or _NULL,
                'url' : kwargs['username'] or _NULL,
                'dir' : kwargs['directory'] or _NULL,
                'oldfile' : kwargs['oldfile'] or _NULL,
                'newfile' : kwargs['newfile'] or _NULL,
                'cmd' : kwargs['cmd'] or _NULL,
                'dataobj' : kwargs['dataobj'] or _NULL,
                'tag' : kwargs['tag'] or _NULL
            }
            session.add(ImCmd(**_entry_data))
            session.commit()
            #FIXME session.close()....
        except Exception as e:
            sys.stderr.write("Unable to commit database entry\n")
            sys.stderr.write(str(e))
