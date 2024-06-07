"""File DataServer to generate the number list using Flask"""
import os
import random
import signal
import json
from rsaencryption import RSAEncryption
from flask import Flask,request,jsonify # type: ignore
from Random.random_normal_distribution import RandomNormalDistribution # pylint: disable=E0401,E0611
from Random.random_uniform_distribution import RandomUniformDistribution # pylint: disable=E0401,E0611


def create_app(test_config=None):
    """ create and configure the app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:

        receiver=RSAEncryption('receiver')
        receiver.generate_keys()
        transmitter_key = None # pylint: disable=W0612
        @app.route('/key', methods=['POST'])
        def key():
            request_data = request.json
            transmitter_key=request_data['public_key']
            with open("transmitter_key.pem","w",encoding='utf-8') as file:
                file.write(transmitter_key)
            receiver_key=receiver.to_json()
            return receiver_key

        @app.route("/numbers", methods=("POST",))
        def numbers():
            request_data = request.json
            parameters_encrypted=request_data['parameters_encrypted']
            parameters_decrypted=receiver.decrypt_message(parameters_encrypted)
            parameters=json.loads(parameters_decrypted)

            cant=parameters['cant']
            limitmin=parameters['min']
            limitmax=parameters['max']

            flag = random.choice([True, False])
            random_numbers = None
            if flag:
                random_way=RandomNormalDistribution()
            else:
                random_way=RandomUniformDistribution()

            random_numbers=random_way.generate_numbers(cant,limitmin,limitmax)
            random_numbers=[str(abs(n)) for n in random_numbers]
            response={'Numbers': random_numbers}
            response_encrypted=receiver.encrypt_message(json.dumps(response),'transmitter_key.pem')
            back={"response_encrypted":response_encrypted}
            return jsonify(back)

        @app.route('/shutdown', methods=['POST'])
        def shutdown():
            shutdown_server()
            return 'Server shutting down...'

    return app

def shutdown_server():
    """Function to close the connection of Flask server"""
    pid = os.getpid()
    os.kill(pid, signal.SIGINT)
