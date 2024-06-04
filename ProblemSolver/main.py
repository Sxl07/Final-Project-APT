import socket
import json
import requests # type: ignore
from FactoryMethod.fizzbuzzcreator import FizzbuzzCreator
from FactoryMethod.fibonaccicreator import FibonacciCreator
from FactoryMethod.primecreator import PrimeCreator
import hashlib
import hmac
from rsaencryption import RSAEncryption
import logging

shutdown_flag = False

def readFileConfiguration():
    config = {}
    with open("config.txt", 'r') as file:
        for line in file:
            line = line.strip()     
            if line:
                key, value = line.split(':', 1)
                config[key.strip()] = value.strip()
    return config.get('KEY'),config.get('PASSWORD')

def hashPassword(password, key):
    h = hmac.new(key.encode(), password.encode(), hashlib.sha256)
    hashed_password = h.hexdigest()
    return hashed_password

def checkPassword(password):
    key,correctPassword=readFileConfiguration()
    hashedP=hashPassword(password,key)
    if correctPassword==hashedP:
        return True
    return False

def solve_problem(problem, parameters, transmitter, receiver_key):
    if problem == "fizzbuzz":
        problemSolver=FizzbuzzCreator()
    if problem == "fibonacci":
        problemSolver=FibonacciCreator()
    if problem == "prime":
        problemSolver=PrimeCreator()

    with open("receiver_key.pem","w") as file:
        file.write(receiver_key)

    parameters_encrypted=transmitter.encrypt_message(json.dumps(parameters),'receiver_key.pem')
    logging.info("Data encrypted")
    send={
        "parameters_encrypted":parameters_encrypted
    }
    logging.info("Sending data encrypt to DataServer")
    response=requests.post('http://localhost:5000/numbers',json=send)
    logging.info("Encrypted response data received by DataServer")
    back_encrypted=response.json()['response_encrypted']
    back_decrypted=transmitter.decrypt_message(back_encrypted)
    logging.info("Response data decrypted")
    numbers=json.loads(back_decrypted)['Numbers']
    logging.info(f'Resolving problem {problem}')
    result=problemSolver.problemSolution(numbers)
    logging.info('Problem solved successfully')
    return result

def handle_client_connection(client_socket,addr):
    global shutdown_flag
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
                if checkPassword(password):
                    print("Shutdown request accepted.")
                    logging.info("Shutdown request accepted")
                    response['Result'] = ["System down"]
                    response_shutdown = json.dumps(response)
                    client_socket.send(response_shutdown.encode('utf-8'))
                    shutdown_flag = True
                    logging.info("Closing client socket")
                    logging.info("Closing Flask server")
                    requests.post('http://localhost:5000/shutdown')
                    break
                else:
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
                key_response=requests.post('http://localhost:5000/key',json=transmitter_key)       
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

                print(f"Resolving problem: {problem} with {values_count} values between {min_value} and {max_value}")
                result = solve_problem(problem, parameters,transmitter,receiver_key)
                response['Result']=result
                response_data = json.dumps(response)
                print(f"Send response: {response_data}")
                client_socket.send(response_data.encode('utf-8'))
                logging.info("Results sent to Client")
            elif request.get('Problem')=="":
                pass
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
        logging.info(f'Reconnected to {addr}')
    except requests.exceptions.ConnectionError:
        print("Flask Connection Down Success")
        logging.info("Flask connection closed")
    finally:
        client_socket.close()

def main():
    logging.basicConfig(filename='app.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)


    global shutdown_flag
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(5)
    print('Server listening at the port 8080...')
    
    while not shutdown_flag:
    
        client_socket, addr = server_socket.accept()
        print('Connection accepted by:', addr)
        logging.info("-------------------------------")
        logging.info(f'Connection accepted by: {addr}')
        handle_client_connection(client_socket,addr) 
    
    server_socket.close()
    logging.info("Socket connection closed")
    print("Server off")
    logging.info("ProblemSolver closed")
if __name__ == '__main__':
    main()
