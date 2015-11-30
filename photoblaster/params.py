"""Params class and methods stored here"""
import sys
from photoblaster.param import Bool, Color, Enum, Float, Int,\
    Img_url, Json, Raw, String

class BadParamError(Exception):
    pass

class Params(object):
    """
    Params is a collection of Param instances,
    Args:
       kwargs: a list of param names and instances,
       as keyword arguments (CURRENTLY UNUSED)
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __iter__(self):
        for key, value in vars(self).iteritems():
            yield key, value

    def _error_log(self, s, error=None, fatal=False):
        message = "ERROR - BAD PARAM"
        if fatal: message += "- [FATAL] -"
        sys.stderr.write("{}:{} - {}\n".format(message, self._classname, s))
        if error:
            sys.stderr.write("PARAM ERROR: {}\n".format(str(error)))

    def err_warn(self, s, error=None):
        self._error_log(s, error=error);
        raise BadParamError("%s - %s" % (self._classname, s))

    def __getattr__(self, key):
        try:
            return self.__getattribute__(key);
        except AttributeError:
            return None

    def definitions_import(self, def_dict, classkwargs, classname=""):
        """main method of this class. takes a dict of definitions,
        along with the keyword arguments of the module and maps them
        to attribute values of the params class"""
        value = None
        for key in def_dict.keys():
            value = None
            if key in classkwargs:
                value = classkwargs.get(key, None) or def_dict[key].get('default', None)
            elif 'default' in def_dict[key]:
                value = def_dict[key]['default']
            if def_dict[key]['type'] == "bool":
                instance = Bool(value, classname=classname)
            elif def_dict[key]['type'] == "color":
                instance = Color(value, classname=classname)
            elif def_dict[key]['type'] == "enum":
                instance = Enum(value, enum_values=def_dict[key]['enum_values'], classname=classname)
            elif def_dict[key]['type'] == "float":
                instance = Float(value, classname=classname)
            elif def_dict[key]['type'] == "img_url":
                instance = Img_url(value, key=key, classname=classname)
            elif def_dict[key]['type'] == "int":
                instance = Int(value, classname=classname)
            elif def_dict[key]['type'] == "json":
                instance = Json(value, classname=classname)
            elif def_dict[key]['type'] == "raw":
                instance = Raw(value, classname=classname)
            elif def_dict[key]['type'] == "string":
                instance = String(value, classname=classname)
            self.__setattr__(key, instance)

