#!/usr/bin/python2.7
"""calls the example_run method on all modules"""
from photoblaster.modules import Pb
for cls in Pb.__subclasses__():
    print cls.__name__
    instance = cls.example_run()
    instance.file_s3move()
    print instance.file_dict()
    instance.db_send();
