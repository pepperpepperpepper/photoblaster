# coding: utf-8
"""describes the ImCmd class"""
from sqlalchemy import Column, Integer, LargeBinary, String
from photoblaster.db.models import Base, Actions

import simplejson as json
from sqlalchemy.orm import class_mapper

class ImCmd(Base, Actions):
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

    def as_dict(self):
        """returns the class as a dictionary

           dataobj is a nested json object that contains more data about the
           command.
           It was made due to poor initial planning, this unpacks it.
        """
        column_names = [c.key for c in class_mapper(self.__class__).columns]
        new_dict = {}
        for c in column_names:
            if c == "dataobj":
                val = getattr(self, c)
                if val is not None:
                    val = json.loads(val)
                new_dict[c] = val
            else:
                new_dict[c] = getattr(self, c)
        return new_dict
