"""Defines the color param type"""
from photoblaster.param import Param
import re
class Color(Param):
    """Defines the color param type
       Args:
           value: the value of the color (string)
           classname: the name of the class to which the param belongs
    """
    def __init__(self, value, classname=""):
        super(Color, self).__init__(classname=classname)
        if value:
            try:
                self.value = self._color_sanitize(value)
            except Exception as e:
                self.err_warn("Unable to sanitize the color: %s" % str(value))
                self.err_warn(str(e))


    def _color_sanitize(self, s):
        if s == "":
            return "transparent"
        if re.match('(rgba?\([0-9]+,[0-9]+,[0-9]+\))|([a-zA-Z]+)|(\#[A-Ha-h0-9]+)', s):
            return s.replace(' ', '')
        else:
            self.err_warn("Not a color: {}\n".format(s))
