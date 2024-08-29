# TCP Server
import socket
import os
import json
import random
import sys
import time

package_list = ["1000001", "1000002", "1000003", "1000004", "1000005", "1000006", "1000007", "1000008", "1000009", "1000010", "1000011", "1000012", "1000013", "1000014", "1000015", "1000016", ]
def start_server(host, port, interval):
    # host = '127.0.0.1'
    # port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"TCP Server listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        data = conn.recv(1024)
        data_de = data.decode()
        if not data:
            break
        else:
            print("TCP server ", host, port, "get: ", data_de)

        # try:
        #     while(True):
        #         data = random.choice(package_list)
        #         conn.sendall(data.encode())
        #         print(data)
        #         time.sleep(3)
        #         # conn.close()

        # except socket.timeout:
        #     print(f"Connection timeout with {addr}")
        #
        # except ConnectionResetError:
        #     print(f"Connection reset by {addr}")
        #
        # except socket.error as e:
        #     print(f"Socket error occurred with {addr}: {e}")

        # finally:
        #     conn.close()
        #     print("Connection is closed.")

        # conn.sendall(data.encode())
        # print(data)
        # # conn.close()

    server_socket.close()


if __name__ == "__main__":
    start_server("192.168.12.116", 9004, 3)  # Run this in one terminal
    # start_server(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))  # Run this in one terminal
    # start_client()  # Uncomment and run this in another terminal
    # start_server("192.168.136.253", 9004, 3)  # Run this in one terminal
