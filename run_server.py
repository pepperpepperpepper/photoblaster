#!/usr/bin/python2
"""script used to run the webserver"""
import sys
from photoblaster.server import Server
from photoblaster.config import LOCAL


server = Server()

if __name__ == "__main__":
    if LOCAL:
        server.run()
    else:
        server.run_wsgi()
