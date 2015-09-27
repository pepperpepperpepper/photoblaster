"""String class definition lives here"""
from .param import Param
import re
class String(Param):
    """String param class definition
    Args:
        value: a string
        classname: name of the class to which the param instance will belong
    """
    def __init__(self, value, classname=""):
        super(String, self).__init__(classname=classname)
        if value:
            try:
                self.value = self.sanitize(value)
            except Exception as e:
                self.err_warn("Unable to sanitize: %s\nreason:%s" % (str(value), str(e)))
        else:
            self.value = ""
    def sanitize(self, s):
        """Removes non-word characters from the string for security reasons"""
        return re.sub(r'\W+', '', s)
