# coding: utf-8
"""table class for iasdfus"""
from sqlalchemy import BigInteger, Column, Integer, String
from photoblaster.db.models import Base, Actions

class Iasdfus(Base, Actions):
    __tablename__ = 'iasdfus'

    id = Column(BigInteger, primary_key=True)
    address = Column(String(1000), index=True)
    last_accessed = Column(BigInteger)
    times_dumped = Column(Integer)
    times_accessed = Column(Integer)
    deleted = Column(Integer)



