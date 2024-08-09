# TCP Client
import socket
import json

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while(True):
        message = input("Scan a bar code:")
        # print(message)
        client_socket.sendall(message.encode())

    # data = client_socket.recv(1024)
    # print(f"Received from server: {data.decode()}")

    client_socket.close()

if __name__ == "__main__":
    with open('local_server.txt', 'r') as file_3:
        server_config = json.loads(file_3.read())

    # start_server()  # Run this in one terminal
    start_client(server_config['ip'], server_config['tcp_port'])  # Uncomment and run this in another terminal