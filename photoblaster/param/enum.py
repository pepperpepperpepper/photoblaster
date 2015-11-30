"""Defines the enum param type"""

from photoblaster.param import Param
class Enum(Param):
    """Defines the enum param type
    Args:
        value: the value of the param
        enum_values: an array of possible value types
        classname: name of the class that the param belongs to
    """
    def __init__(self, value, enum_values=[], classname=""):
        super(Enum, self).__init__(classname=classname)
        if value and value not in enum_values:
            self.err_warn("Value %s not in enum values" % str(value))
        self.value = value
