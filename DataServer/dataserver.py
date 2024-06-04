import json
import os
import random
import signal
import sys
from flask import Flask,request,jsonify # type: ignore

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

        @app.route("/numbers", methods=("POST",))
        def numbers():
            request_data = request.json
            cant=request_data['cant']
            limitmin=request_data['min']
            limitmax=request_data['max']
            
            random_numbers = [str(random.randint(limitmin,limitmax)) for _ in range(cant)]
            response_json = {'Numbers': random_numbers}
            return jsonify(response_json)
        
        @app.route('/shutdown', methods=['POST'])
        def shutdown():
            shutdown_server()
            return 'Server shutting down...'

    return app

def shutdown_server():
    pid = os.getpid()
    os.kill(pid, signal.SIGINT)