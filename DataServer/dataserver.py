import os
import random
import signal
import json
from Random.randomNormalDistribution import RandomNormalDistribution
from Random.randomUniformDistribution import RandomUniformDistribution
from flask import Flask,request,jsonify # type: ignore
from rsaencryption import RSAEncryption

def create_app(test_config=None):
    # create and configure the app
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
        pass
        receiver=RSAEncryption('receiver')
        receiver.generate_keys()
        transmitter_key = None
        @app.route('/key', methods=['POST'])
        def key():
            request_data = request.json
            transmitter_key=request_data['public_key']
            with open("transmitter_key.pem","w") as file:
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
                randomWay=RandomNormalDistribution()
            else:
                randomWay=RandomUniformDistribution()
            random_numbers=randomWay.generateNumbers(cant,limitmin,limitmax)
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
    pid = os.getpid()
    os.kill(pid, signal.SIGINT)