from os import getenv
import socket
import json
import requests
from FactoryMethod.fizzbuzzcreator import FizzbuzzCreator
from FactoryMethod.fibonaccicreator import FibonacciCreator
from FactoryMethod.primecreator import PrimeCreator
import hashlib
import hmac

shutdown_flag = False

def leer_archivo_configuracion():
    config = {}
    with open("config.txt", 'r') as archivo:
        for linea in archivo:
            linea = linea.strip()     
            if linea:
                clave, valor = linea.split(':', 1)
                config[clave.strip()] = valor.strip()
    return config.get('KEY'),config.get('PASSWORD')

def hash_password(password, key):
    h = hmac.new(key.encode(), password.encode(), hashlib.sha256)
    hashed_password = h.hexdigest()
    return hashed_password

def checkPassword(password):
    key,correctPassword=leer_archivo_configuracion()
    hashedP=hash_password(password,key)
    if correctPassword==hashedP:
        return True
    return False

def solve_problem(problem, values_count, min_value, max_value):
    parameters={
            "cant":values_count,
            "min":min_value,
            "max":max_value,
        }
    if problem == "fizzbuzz":
        problemSolver=FizzbuzzCreator()
    if problem == "fibonacci":
        problemSolver=FibonacciCreator()
    if problem == "prime":
        problemSolver=PrimeCreator()
    else:
        result = []
    response=requests.post('http://localhost:5000/numbers',json=parameters)
    numbers=response.json()["Numbers"]
    result=problemSolver.problemSolution(numbers)
    return result

def handle_client_connection(client_socket,addr):
    global shutdown_flag
    try:
        while True:
            request_data = client_socket.recv(1024)
            if not request_data:
                break
            print(f"Solicitud recibida: {request_data.decode('utf-8')}")
            request = json.loads(request_data.decode('utf-8'))

            response_shut = {
                'Result': [""]
            }

            shutdown = request.get('Shutdown')
            password = request.get('Password')
            if shutdown == 1:
                if checkPassword(password):
                    print("Solicitud de apagado recibida.")
                    response_shut['Result'] = ["System down"]
                    response_shutdown = json.dumps(response_shut)
                    client_socket.send(response_shutdown.encode('utf-8'))
                    shutdown_flag = True
                    requests.post('http://localhost:5000/shutdown')
                    break
                else:
                    print("Solicitud de apagado denegada, contraseña incorrecta.")
                    response_shut['Result'] = ["Incorrect password"]
                    response_shutdown = json.dumps(response_shut)
                    client_socket.send(response_shutdown.encode('utf-8'))

            if request.get('Problem') != "":
                problem = request.get('Problem')
                values_count = int(request.get('Cant'))
                min_value = int(request.get('Min'))
                max_value = int(request.get('Max'))

                print(f"Resolviendo problema: {problem} con {values_count} valores entre {min_value} y {max_value}")

                result = solve_problem(problem, values_count, min_value, max_value)
                response = {
                    'Result': result
                }
                response_data = json.dumps(response)
                print(f"Enviando respuesta: {response_data}")
                client_socket.send(response_data.encode('utf-8'))
    except ConnectionResetError:
        print(f"Reconnecting to client_socket...")
        print('Conexión aceptada de:', addr)
    except requests.exceptions.ConnectionError:
        print("Flask Down")
    finally:
        client_socket.close()

def main():
    global shutdown_flag
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(5)
    print('Servidor escuchando en el puerto 8080...')
    
    while not shutdown_flag:
    
        client_socket, addr = server_socket.accept()
        print('Conexión aceptada de:', addr)
        handle_client_connection(client_socket,addr)
        
    
    server_socket.close()
    print("Servidor apagado.")

if __name__ == '__main__':
    main()
