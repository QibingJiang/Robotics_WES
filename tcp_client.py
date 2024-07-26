# TCP Client
import socket


def start_client():
    host = '127.0.0.1'
    # port = 12345
    port = 23

    # host = '192.168.1.154'
    host = '127.0.0.1'
    port = 9004


    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    message = "Hello, server!"
    client_socket.sendall(message.encode())

    data = client_socket.recv(1024)
    print(f"Received from server: {data.decode()}")

    client_socket.close()

if __name__ == "__main__":
    # start_server()  # Run this in one terminal
    start_client()  # Uncomment and run this in another terminal