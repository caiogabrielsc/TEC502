import datetime
import pickle
import socket
import time
import threading

device_data = {'active': True,'turbo':True,'city_temp':34,'actual_temp': 34,'goal_temp':18,'turn_on_time':datetime.datetime.now()}

def temp_handler():
    while True:
        time.sleep(1)
        if device_data['active'] == True and device_data['actual_temp'] > device_data['goal_temp']: 
                # DESCE A TEMP ATÈ CHEGAR NO GOALTEMP
            if device_data['turbo']== True:
                device_data['actual_temp'] += -0.3
            if device_data['turbo']== False:
                device_data['actual_temp'] += -0.1
        else:          # SE ESTÀ DESLIGADO - SOBE ATÈ A CITY TEMP
            if device_data['actual_temp'] < device_data['city_temp']:
                device_data['actual_temp'] += 0.3
                     
def send_data_to_broker():
    SERVER_HOST = 'localhost'  
    SERVER_PORT = 50000        
    connected = False

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while not connected:
            try:    
                s.connect((SERVER_HOST, SERVER_PORT))
                connected = True
            except ConnectionRefusedError:
                time.sleep(1)
        while True:            
            s.sendall(pickle.dumps(device_data))
            time.sleep(1)
         
def recive_commands():
    HOST = 'localhost'  
    PORT = 60000   

    def command_handler(data, addr):
        command = data.decode()

        if command == 'turnoff':
            device_data['active'] = False
        if command == 'turnon' and device_data['active'] == False:
            device_data['active'] = True
            device_data['turn_on_time'] = datetime.datetime.now()
        if command.startswith('settemp'):
            command, value = command.split()
            device_data['goal_temp'] = float(value)
        if command.startswith('setmode'):
            command, mode = command.split()
            if mode == 'turbo':
                device_data['turbo'] = True
            if mode == 'normal':
                device_data['turbo'] = False
        print(f'Command {command} recived.')
        
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        while True:
            data, addr = s.recvfrom(1024)
            threading.Thread(target=command_handler, args=(data, addr)).start()

threading.Thread(target=temp_handler).start()
threading.Thread(target=send_data_to_broker).start()
threading.Thread(target=recive_commands).start()
