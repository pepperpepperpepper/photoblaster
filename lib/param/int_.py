"""Int class definition lives here"""
from .param import Param

class Int(Param):
    def __init__(self, value, classname=""):
        """Defines the float param type
           Args:
               value: the value of the Int
               classname: the name of the class to which the param belongs
        """
        super(Int, self).__init__(classname=classname)
        try:
            if value:
                self.value = int(value)
            else:
                self.value = 0
        except Exception as e:
            self.err_warn("Not an int: %s" % str(value))
            self.err_warn(str(e))

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)
