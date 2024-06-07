"""Main file (ProblemSolver)"""
import hashlib
import hmac
import socket
import json
import logging
import requests # type: ignore
from rsaencryption import RSAEncryption
from FactoryMethod.fizzbuzzcreator import FizzbuzzCreator
from FactoryMethod.fibonaccicreator import FibonacciCreator
from FactoryMethod.primecreator import PrimeCreator

SHUTDOWN_FLAG = False

def read_file_configuration():
    """function to read the config file"""
    config = {}
    with open("config.txt", 'r',encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split(':', 1)
                config[key.strip()] = value.strip()
    return config.get('KEY'),config.get('PASSWORD')

def hash_password():
    """function to hash the correct password"""
    key,correct=read_file_configuration()
    if isinstance(correct, str):
        correct = correct.encode()
    if isinstance(key, str):
        key = key.encode()

    hmac_obj = hmac.new(key, correct, hashlib.sha256)
    return hmac_obj.hexdigest()

def check_password(password):
    """function to check the password to shutdown"""
    correct_password=hash_password()
    if password==correct_password:
        return True
    return False

def solve_problem(problem, parameters, transmitter, receiver_key):
    """function to do the process of solve problems"""
    if problem == "fizzbuzz":
        problem_solver=FizzbuzzCreator()
    if problem == "fibonacci":
        problem_solver=FibonacciCreator()
    if problem == "prime":
        problem_solver=PrimeCreator()

    with open("receiver_key.pem","w",encoding='utf-8') as file:
        file.write(receiver_key)

    parameters_encrypted=transmitter.encrypt_message(json.dumps(parameters),'receiver_key.pem')
    logging.info("Data encrypted")
    send={
        "parameters_encrypted":parameters_encrypted
    }
    logging.info("Sending data encrypt to DataServer")
    response=requests.post('http://localhost:5000/numbers',json=send,timeout=60)
    logging.info("Encrypted response data received by DataServer")
    back_encrypted=response.json()['response_encrypted']
    back_decrypted=transmitter.decrypt_message(back_encrypted)
    logging.info("Response data decrypted")
    numbers=json.loads(back_decrypted)['Numbers']
    logging.info('Resolving problem %s',problem)
    result=problem_solver.problem_solution(numbers)
    logging.info('Problem solved successfully')
    return result

def handle_client_connection(client_socket,addr):# pylint: disable=R0914,R0915
    """Function to manage the code flow, mainly the socket connection"""
    global SHUTDOWN_FLAG
    try:
        while True:
            request_data = client_socket.recv(1024)
            if not request_data:
                break
            print(f"Request received: {request_data.decode('utf-8')}")
            logging.info("Request data received by Client")
            request = json.loads(request_data.decode('utf-8'))

            response = {
                'Result': None
            }

            shutdown = request.get('Shutdown')
            password = request.get('Password')
            if shutdown == 1:
                logging.info("Shutdown request received")
                if check_password(password):
                    print("Shutdown request accepted.")
                    logging.info("Shutdown request accepted")
                    response['Result'] = ["System down"]
                    response_shutdown = json.dumps(response)
                    client_socket.send(response_shutdown.encode('utf-8'))
                    SHUTDOWN_FLAG = True
                    logging.info("Closing client socket")
                    logging.info("Closing Flask server")
                    requests.post('http://localhost:5000/shutdown',timeout=60)
                    break
                print("Shutdown request denied, incorrect password.")
                logging.info("Shutdown request denied(Incorrect password)")
                response['Result'] = ["Incorrect password"]
                response_shutdown = json.dumps(response)
                client_socket.send(response_shutdown.encode('utf-8'))

            problems=["fizzbuzz","fibonacci","prime"]
            if request.get('Problem') in problems:
                transmitter=RSAEncryption('transmitter')
                transmitter.generate_keys()
                transmitter_key=transmitter.to_json()
                key_response=requests.post('http://localhost:5000/key',json=transmitter_key,timeout=60)# pylint: disable=C0301
                receiver_key=key_response.json()['public_key']
                logging.info("Public encryption keys exchanged")

                problem = request.get('Problem')
                values_count = int(request.get('Cant'))
                min_value = int(request.get('Min'))
                max_value = int(request.get('Max'))
                parameters={
                "cant":values_count,
                "min":min_value,
                "max":max_value,
                }

                print(f"Resolving problem: {problem} with {values_count} values between {min_value} and {max_value}")# pylint: disable=C0301
                result = solve_problem(problem, parameters,transmitter,receiver_key)
                response['Result']=result
                response_data = json.dumps(response)
                print(f"Send response: {response_data}")
                client_socket.send(response_data.encode('utf-8'))
                logging.info("Results sent to Client")
            else:
                response = {
                    'Result': ["Problem not found"]
                }
                response_data=json.dumps(response)
                client_socket.send(response_data.encode('utf-8'))
                logging.info("Problem not found")

    except ConnectionResetError:
        print(f"Reconnecting to client_socket...")
        print('Connection accepted by:', addr)
        logging.info('Reconnected to %s',addr)
    except requests.exceptions.ConnectionError:
        print("Flask Connection Down Success")
        logging.info("Flask connection closed")
    finally:
        print("Client socket closed")
        logging.info("Client socket closed")
        client_socket.close()

def main():
    """main"""
    logging.basicConfig(filename='app.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

    global SHUTDOWN_FLAG
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(5)
    print('Server listening at the port 8080...')

    while not SHUTDOWN_FLAG:
        client_socket, addr = server_socket.accept()
        print('Connection accepted by:', addr)
        logging.info("-------------------------------")
        logging.info('Connection accepted by: %s',addr)
        handle_client_connection(client_socket,addr)

    server_socket.close()
    logging.info("Socket connection closed")
    print("Server socket off")
    logging.info("ProblemSolver closed")
if __name__ == '__main__':
    main()
