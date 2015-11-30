"""Defines the bool param type"""
from photoblaster.param import Param
import re
class Bool(Param):
    """Defines the bool param type
    Args:
        value: the value of the bool (string or python bool)
        classname: the name of the class to which the param belongs
    """
    def __init__(self, value, classname=""):
        super(Bool, self).__init__(classname=classname)
        if value:
            self.value = self._bool_correct(value)
        else:
            self.value = False
    def _bool_correct(self, b):
        if isinstance(b, str) or isinstance(b, unicode):
            if re.match(r'true', b, re.IGNORECASE):
                return True
            elif re.match(r'false', b, re.IGNORECASE):
                return False
        elif isinstance(b, bool):
            return b
        self.err_warn("Not a bool: %s" % str(b))
