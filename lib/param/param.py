"""param base class lives here, used for inheritance only"""
import time
import sys

from config import WORKING_DIR

class BadParamError(Exception):
    pass


class Param(object):
    """Defines the param base class, this class is used for inheritance only"""
    def __init__(self, classname="", **kwargs):
        self.value = None
        self._working_dir = WORKING_DIR
        self._now = kwargs.get("now", str(int(time.time())))
        self._classname = classname
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __nonzero__(self):
        return True if self.value else False

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def set_val(self, value):
        try:
            self.value = value
        except Exception as e:
            self.err_warn("Unable to set value {}".format(value))

    def err_warn(self, s):
        self._error_log(s)
        raise BadParamError("%s - %s\n" % (self._classname, s))

    def __getattr__(self, key):
        try:
            return self.__getattribute__(key)
        except AttributeError:
            return None

    def err_fatal(self, s, error=None):
        self._log(s, error, fatal=True)
        sys.exit(1)

    def _error_log(self, s, fatal=False):
        message = "ERROR - BAD PARAM"
        if fatal: message += "- [FATAL] -"
        sys.stderr.write("{}:{} - {}\n".format(message, self._classname, s))

