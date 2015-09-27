"""Defines the json param type"""
from .param import Param
import simplejson as json

class Json(Param):
    """Defines the json param type. Loads in a
    json value and parses it.

    Args:
        value: a json string
        classname: name of the class to which the param belongs
    """
    def __init__(self, value, classname=""):
        super(Json, self).__init__(classname=classname)
        self.value = json.loads(value)
