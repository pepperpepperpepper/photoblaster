"""Defines the raw param type"""
from .param import Param

class Raw(Param):
    """Defines the raw param type.
    Basically, this is a catchall class, any input can go here,
    so it needs to be used carefully (for security reasons).
    Args:
       value: can be any value
       classname: name of the class to which the param instance belongs
    """
    def __init__(self, value, classname=""):
        super(Raw, self).__init__(classname=classname)
        self.value = value or None
