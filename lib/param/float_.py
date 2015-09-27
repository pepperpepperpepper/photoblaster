"""Defines the float param type"""
from .param import Param
class Float(Param):
    """Defines the float param type
       Args:
           value: the value of the Float
           classname: the name of the class to which the param belongs
    """
    def __init__(self, value, classname=""):
        self._classname = classname
        super(Float, self).__init__(classname=classname)
        try:
            if value:
                self.value = float(value)
            else:
                self.value = 0.0
        except Exception as e:
            self.err_warn("Not a float: %s" % str(value))
            self.err_warn(str(e))
    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)
