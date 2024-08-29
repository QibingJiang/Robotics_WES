# TCP Client
import socket
import json
import time

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        try:
            message = input("Scan a bar code: ")
            if message.strip() == '':  # Exit loop if input is empty
                print("No input provided. Exiting.")
                break
            client_socket.sendall(message.encode())
        except (socket.error, ConnectionResetError) as e:
            print(f"Socket error occurred: {e}. Close TCP connection.")
            client_socket.close()
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
        finally:
            pass

if __name__ == "__main__":
    with open('local_server.txt', 'r') as file_3:
        server_config = json.loads(file_3.read())

    while True:
        try:
            start_client(server_config['ip'], server_config['tcp_port'])
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Restarting...")
            time.sleep(1)
