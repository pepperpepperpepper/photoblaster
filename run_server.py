#!/usr/bin/python2
"""used to run the webserver"""
import sys
sys.path.append("./lib")
from server import Server
server = Server()

if __name__ == "__main__":
    server.run_wsgi()

