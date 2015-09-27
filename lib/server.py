"""All webserver logic lives here, including routes"""
from flask import Flask
from flask import request, jsonify
import sys
import cherrypy
from paste.translogger import TransLogger

sys.path.append("./lib")
from pb import *
from param import BadParamError
from config import SERVER_HOST, SERVER_PORT


class InvalidUsage(Exception):
    """error class for InvalidUsage"""
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class Server(object):
    """Main server class"""
    def __init__(self):
        self.app = Flask(__name__)
        self._wsgi_server = None

        @self.app.route('/test', methods=['GET'])
        def test():
            return "HELLO WORLD!"

        @self.app.route('/im/api/<pb_classname>', methods=['POST'])
        def pb(pb_classname):
            return self._response_post(pb_classname, request.form.to_dict())

        @self.app.errorhandler(InvalidUsage)
        def handle_invalid_usage(error):
            response = jsonify(error.to_dict())
            response.status_code = error.status_code
            return response

        self._classname_aliases = {
            'generate': 'PbGenerate',
            'imgrid': 'PbGrid',
            'imbreak': 'PbBreaker',
            'impattern': 'PbPattern',
            'imgradient': 'PbGradient',
        }

    def _find_class_by_name(self, pb_classname):
        pb_classname = self._classname_aliases.get(pb_classname, None) or \
            pb_classname
        try:
            return filter(
                lambda c: c.__name__ == pb_classname, Pb.__subclasses__()
            )[0]
        except IndexError:
            raise InvalidUsage('No such api', status_code=410)

    def _response_post(self, pb_classname, request_form):
        pb_class = self._find_class_by_name(pb_classname)
        try:
            pb = pb_class(**request_form)
            pb.create()
            pb.file_s3move()
            pb.db_send()
            return jsonify(pb.file_dict())

        except BadParamError:
            return jsonify({'error': 'Bad Params'})
        except PbProcessError:
            return jsonify({'error': 'Problem with server-side processing'})

    def run(self, host=SERVER_HOST, port=SERVER_PORT):
        self.app.run(host=host, port=port)

    def run_wsgi(self, server_port=SERVER_PORT, host=SERVER_HOST):
        # Enable WSGI access logging via Paste
        app_logged = TransLogger(self.app)

        # Mount the WSGI callable object (app) on the root directory
        cherrypy.tree.graft(app_logged, '/')

        # Set the configuration of the web server
        cherrypy.config.update({
            'engine.autoreload_on': True,
            'log.screen': True,
            'server.socket_port': server_port,
            'server.socket_host': host
        })
        cherrypy.engine.start()
        cherrypy.engine.block()
