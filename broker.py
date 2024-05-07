import datetime
import os
import pickle
import time
import socket
import threading

can_print = True

def recive_data():
    HOST = 'localhost'  
    PORT = 50000

    def print_data(data):
        os.system('clear')
        current_time = datetime.datetime.now()
        time_since_turn_on = (current_time - data['turn_on_time']).total_seconds()
        print("-" * 40)
        print(f"Active: {data['active']}\t\tTurbo: {data['turbo']}")
        print(f"City Temp: {data['city_temp']:.1f}°C  \tActual Temp: {data['actual_temp']:.1f}°C  \tGoal Temp: {data['goal_temp']:.1f}°C")
        print(f"Time On: {int(time_since_turn_on)} seconds")
        print("-" * 40)
        
    def handle_device_connection(conn, addr):
        print('Conectado por', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            device_data = pickle.loads(data)
            if device_data['active'] == True:
                print_data(device_data)
            else:
                os.system('clear')
                print('Device off')
        conn.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Aguardando conexão do dispositivo...')
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_device_connection, args=(conn, addr)).start()

def send_commands():
    SERVER_HOST = 'localhost'  
    SERVER_PORT = 60000        
    global can_print

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        while True:

            # DEMONSTRAÇÃO DOS COMANDOS

            time.sleep(10)
            command = 'settemp -20'
            s.sendto(str(command).encode(), (SERVER_HOST, SERVER_PORT))       
            time.sleep(4)
            command = 'settemp -100'
            s.sendto(str(command).encode(), (SERVER_HOST, SERVER_PORT))       
            time.sleep(4)
            command = 'turnoff'
            s.sendto(str(command).encode(), (SERVER_HOST, SERVER_PORT))       
            time.sleep(4)
            command = 'turnon'
            time.sleep(4)
            s.sendto(str(command).encode(), (SERVER_HOST, SERVER_PORT))       
            time.sleep(4)
            command = 'setmode normal'
            s.sendto(str(command).encode(), (SERVER_HOST, SERVER_PORT))       
            time.sleep(4)
            command = 'setmode turbo'
            s.sendto(str(command).encode(), (SERVER_HOST, SERVER_PORT))       

threading.Thread(target=recive_data).start()
threading.Thread(target=send_commands).start()
