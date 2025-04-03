# HTTP Server
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import jwt
import asyncio
import websockets
import threading
import random
import socket
import os
import re

# class RCS:
#     def __init__(self):
#         self.IP = ""
#         self.WS_client = None
#         # self.chutes = []

# RCS_a = RCS()
# # RCS_a.chutes = ["2A20", "2A19", "2A18", "2A17", "2A16", "2A15", "2A14", "2A13", "2A12", "2A11", "2A10", "2A09", "2A08", "2A07", "2A06", "2A05", "2A04", "2A03", "2A02", "2A01", "2B20", "2B19", "2B18", "2B17", "2B16", "2B15", "2B14", "2B13", "2B12", "2B11", "2B10", "2B09", "2B08", "2B07", "2B06", "2B05", "2B04", "2B03", "2B02", "2B01", "2C20", "2C19", "2C18", "2C17", "2C16", "2C15", "2C14", "2C13", "2C12", "2C11", "2C10", "2C09", "2C08", "2C07", "2C06", "2C05", "2C04", "2C03", "2C02", "2C01", "2D20", "2D19", "2D18", "2D17", "2D16", "2D15", "2D14", "2D13", "2D12", "2D11", "2D10", "2D09", "2D08", "2D07", "2D06", "2D05", "2D04", "2D03", "2D02", "2D01", "2JP01"]

IP2chutes = None # Used for randomly sort.
if(os.path.exists('./RCSs_for_random_sort.txt')):
    file_p = open('./RCSs_for_random_sort.txt', 'r')
    IP2chutes = json.loads(file_p.read())

ws_clients = {} # IP to websocket clients
# clients["127.0.0.1"] = RCS_a

file_1 = open('cameras.txt', 'r')
cam_config = file_1.read()
cams = json.loads(cam_config)

ip_cam = {}
# induction_cam = {}
induction_bot = {}

cam_ips = cams.keys()

# for cam_ip in cam_ips:
#     ip_cam[cam_ip] = cams[cam_ip]
#
#     inductions = cams[cam_ip]["inductions"]
#     for IP in inductions.keys():
#         k = (IP, inductions[IP])
#         if(k not in induction_cam):
#             induction_cam[k] = []
#         induction_cam[k].append(cam_ip)



file_p = "./package2chute.txt"
if os.path.exists(file_p):
    file_2 = open(file_p, 'r')
    package2chute = file_2.read()
    package2chute = json.loads(package2chute)
    # pass
else:
    print(file_p, "does not exist.")
    print("If you want to simulate randomly, rerun the program and specify it.")
    exit()

mode = 'sort'
# mode = 'random'

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, this is the HTTP server!")

    def do_POST(self):
        # print("Http server get post")

        # Get client IP address
        client_ip, client_port = self.client_address

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)
        # print("http post: ", data)

        if('username' in data):

            print("Http client:", client_ip, data["username"])
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            # Define a secret key (for demonstration purposes; use a secure secret in production)
            SECRET_KEY = "my-secret-key"

            # Create a payload (claims) for the JWT
            payload = {
                "sub": "admin@facility1.company1.com",
                "firstName": "API",
                "lastName": "User",
                "companyCode": "Company1",
                "companyTimeZone": "-08:00",
                "scopes": [
                    "api_user"
                ],
                "iss": "http://www.tompksinsinc.com",
                "iat": 1714926400,
                "exp": 4735008000
            }

            # Encode the payload into a JWT
            encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS512")
            # print(f"Encoded JWT: {encoded_jwt}")

            data = {
                "token":encoded_jwt,
                "refreshToken":encoded_jwt
            }
            json_input_string = json.dumps(data)

            self.wfile.write(json_input_string.encode())

        elif('messageNumber' in data):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            if(data['messageCode'] == 'ROBOTSTATUSUPDATE'):

                # if((client_ip, data['currentLocationId']) in induction_cam):
                k = str((client_ip, data['currentLocationId']))
                if(k in induction_bot):
                    induction_bot[k][0] = data['robotId']
                else:
                #    induction_bot[k] = ['','']
                    induction_bot[k] = [data['robotId'],'']
                    print("I add this line on 02182025, testing")
                    print(data)
                    print(k, data['robotId'])
                
                # else:
                #     # print("No camera is specified for ", client_ip, data['currentLocationId'])
                #     pass

        else:
            print("get unknown message:", data)
            pass

def start_http_server(host, port):

    server = HTTPServer((host, port), MyHTTPRequestHandler)
    print(f"HTTP server listening on {host}:{port}")
    server.serve_forever()

async def echo(websocket):
    # print("one websocket get connected.", websocket)

    client_ip = websocket.remote_address[0]
    if(client_ip == '::1'):
        client_ip = '127.0.0.1'

    local_ip, local_port = websocket.local_address

    ws_clients[client_ip] = websocket
    print(f"Websocket Client {client_ip} connected.")

    try:
        async for message in websocket:
            print(message)
            # await websocket.send(message)

    except Exception as e:
        print(f"WebSocket error: {e} local:{local_ip} {local_port}, remote:{client_ip}")
        # websocket.close
    finally:
        # Remove the client from the dictionary and close the WebSocket connection
        if client_ip in ws_clients:
            del ws_clients[client_ip]
        await websocket.close()
        print(f"WebSocket Client {client_ip} disconnected.")

async def listen_for_messages(websocket):
    async for message in websocket:
        print(f"Received from server: {message}")
        data = json.loads(message.decode('utf-8'))
        port = 0
        if('port' in cams[data["IP"]]):
            port = cams[data["IP"]]["port"]
        print(data["code"], data["IP"], port)
        await src2dst(data["code"], data["IP"], port, IsCamera=False)

async def broad(websocket):
    # print("one websocket get connected.", websocket)

    client_ip = websocket.remote_address[0]
    if(client_ip == '::1'):
        client_ip = '127.0.0.1'

    local_ip, local_port = websocket.local_address

    print(f"Websocket Client {client_ip} connected.")

    asyncio.create_task(listen_for_messages(websocket))

    try:
        while(True):
            data = {
                'cams':cams,
                'induction_bot':induction_bot
            }
            # print(data)
            # print(json.dumps(data).encode())
            await websocket.send(json.dumps(data).encode())
            await asyncio.sleep(0.5)

            # message = await asyncio.wait_for(websocket.recv(), timeout=0.5)
            # print(f"Received from server: {message}")



    except Exception as e:
        print(f"WebSocket error: {e} local:{local_ip} {local_port}, remote:{client_ip}")
        # websocket.close
    finally:
        await websocket.close()
        print(f"WebSocket Client {client_ip} disconnected.")


async def start_websocket_server(IP, port, function):
    async with websockets.serve(function, IP, port) as ws_sever:
        # print("Web socket server ", IP, "listening at ", port)
        print(f"Web socket server listening on {IP}:{port} {function.__name__} \n")

        await asyncio.Future()  # Run forever

# Function to start the WebSocket server in a separate asyncio event loop
def start_websocket_server_in_thread(IP, port, function):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_websocket_server(IP, port, function))
    loop.run_forever()

async def send_websocket_message(message, websocket):
    print(message)
    try:
        await websocket.send(json.dumps(message).encode())
    except Exception as e:
        print(f"Failed to send message: {e}")

KEEP_ALIVE_INTERVAL = 600  # Adjust this as needed

def handle_TCP_client(conn, addr):
    print(f"TCP Server Connected by {addr}")
    client_ip, client_port = addr
    conn.settimeout(KEEP_ALIVE_INTERVAL)  # Set a timeout for the connection

    while True:
        try:
            data = conn.recv(1024)  # Buffer size is 1024 bytes
            if not data:
                break

        except socket.timeout:
            # Handle keep-alive timeout
            print(f"Connection to {addr} timed out, TCP connection is closing.")
            conn.close()
            break

        except Exception as e: # Maybe the TCP client is closed.
            print(e)
            conn.close()
            break

        data = data.decode()
        data = re.sub(r"[\x02\r\n\s]", "", data)
        # data = data[5:-3]
        print(f"Received from {addr}: {data}")
        # conn.sendall(data)  # Echo the received data back to the client

        asyncio.run(src2dst(data, client_ip, client_port))


def start_TCP_server(HOST, PORT):
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"TCP Server listening on {HOST}:{PORT}")

        while True:
            try:
                conn, addr = server_socket.accept()
                # Start a new thread to handle the client
                client_thread = threading.Thread(target=handle_TCP_client, args=(conn, addr))
                client_thread.start()

            except Exception as e:
                print(f"Error accepting connection: {e}")

# def src2dst(data, cam_ip, cam_port):
#     sortResponse = {
#         "status": "success",
#         "statusCode": 0,
#         "statusDesc": "Message Processed Successfully",
#         "messageNumber": "1",
#         "payload": {
#             "messageCode": "SORTRESPONSE",
#             "stationId": "",  # Station2U
#             "robotId": "",  # "1"
#             "systemAction": 1,
#             "userAction": "",
#             "userMessage": "",
#             "destinationId": "",
#             "productCode": "750000007515",
#             "sku": ""
#         }
#     }
#
#     # cam = ip_cam[(cam_ip, cam_port)]
#     cam = ip_cam[cam_ip]
#
#     s = 0
#     e = len(data)
#
#     if("prefix" in cam):
#         prefix = re.sub(r"[\x02\r\n\s]", "", cam["prefix"])
#         s = len(prefix)
#
#     if("suffix" in cam):
#         suffix = re.sub(r"[\x02\r\n\s]", "", cam["suffix"])
#         e = len(data) - len(suffix)
#
#     data = data[s:e]
#
#     if(data in package2chute):
#
#         dst_ip = package2chute[data][0]
#
#         sortResponse['payload']['stationId'] = cam["inductions"][dst_ip][0]
#
#         if (len(cam["inductions"][dst_ip]) < 2 or cam["inductions"][dst_ip][1] == ''):
#             print("No robot at induction: ", dst_ip, cam["inductions"][dst_ip][0], "\n")
#         else:
#             sortResponse['payload']['robotId'] = cam["inductions"][dst_ip][1]
#             if (mode == 'sort'):
#                 sortResponse['payload']['destinationId'] = package2chute[data][1]
#             else:
#                 sortResponse['payload']['destinationId'] = random.choice(IP2chutes[dst_ip])
#
#             print(sortResponse)
#
#             asyncio.run(send_websocket_message(sortResponse, ws_clients[dst_ip]))
#
#             cam["inductions"][dst_ip][1] = ''
#     else:
#         print("Unknown package ID scaned from Camera:", data)
#         print(package2chute)

# def src2dst(data, cam_ip, cam_port):
#     sortResponse = {
#         "status": "success",
#         "statusCode": 0,
#         "statusDesc": "Message Processed Successfully",
#         "messageNumber": "1",
#         "payload": {
#             "messageCode": "SORTRESPONSE",
#             "stationId": "",  # Station2U
#             "robotId": "",  # "1"
#             "systemAction": 1,
#             "userAction": "",
#             "userMessage": "",
#             "destinationId": "",
#             "productCode": "750000007515",
#             "sku": ""
#         }
#     }
#
#     # cam = ip_cam[(cam_ip, cam_port)]
#     cam = ip_cam[cam_ip]
#
#     s = 0
#     e = len(data)
#
#     if("prefix" in cam):
#         prefix = re.sub(r"[\x02\r\n\s]", "", cam["prefix"])
#         s = len(prefix)
#
#     if("suffix" in cam):
#         suffix = re.sub(r"[\x02\r\n\s]", "", cam["suffix"])
#         e = len(data) - len(suffix)
#
#     barcode = data[s:e]
#
#     if(barcode in package2chute):
#
#         dst_ip = package2chute[barcode][0]
#
#         induction = sortResponse['payload']['stationId'] = cam["inductions"][dst_ip]
#
#         k = (dst_ip, induction)
#
#         if (k not in induction_bot):
#             print("No robot at induction: ", k, "\n")
#         else:
#             sortResponse['payload']['robotId'] = induction_bot[k]
#             # if (mode == 'sort'):
#             sortResponse['payload']['destinationId'] = package2chute[barcode][1]
#             # else:
#             #     sortResponse['payload']['destinationId'] = random.choice(IP2chutes[dst_ip])
#
#             print(barcode, dst_ip, sortResponse['payload']['stationId'], sortResponse['payload']['robotId'], '-->', sortResponse['payload']['destinationId'])
#
#             asyncio.run(send_websocket_message(sortResponse, ws_clients[dst_ip]))
#
#             del induction_bot[k]
#
#     else:
#         print("Unknown package ID scaned from Camera:", barcode)
#         print(package2chute)

async def src2dst(data, cam_ip, cam_port, IsCamera = True):
    sortResponse = {
        "status": "success",
        "statusCode": 0,
        "statusDesc": "Message Processed Successfully",
        "messageNumber": "1",
        "payload": {
            "messageCode": "SORTRESPONSE",
            "stationId": "",  # Station2U
            "robotId": "",  # "1"
            "systemAction": 1,
            "userAction": "",
            "userMessage": "",
            "destinationId": "",
            "productCode": "750000007515",
            "sku": ""
        }
    }

    # cam = ip_cam[(cam_ip, cam_port)]
    # cam = cams[cam_ip]

    s = 0
    e = len(data)


    if(IsCamera):
        if("prefix" in cams[cam_ip]):
            prefix = re.sub(r"[\x02\r\n\s]", "", cams[cam_ip]["prefix"])
            s = len(prefix)

        if("suffix" in cams[cam_ip]):
            suffix = re.sub(r"[\x02\r\n\s]", "", cams[cam_ip]["suffix"])
            e = len(data) - len(suffix)

    barcode = data[s:e]

    cams[cam_ip]["code"] = barcode

    if(barcode in package2chute):

        dst_ip = package2chute[barcode][0]

        induction = sortResponse['payload']['stationId'] = cams[cam_ip]["inductions"][dst_ip]

        k = str((dst_ip, induction))

        if (k not in induction_bot or induction_bot[k][0] == ''):
            print("No robot at induction: ", k, "\n")
        else:
            sortResponse['payload']['robotId'] = induction_bot[k][0]
            sortResponse['payload']['destinationId'] = package2chute[barcode][1]
            sortResponse['payload']['productCode'] = barcode

            # print(barcode, dst_ip, sortResponse['payload']['stationId'], sortResponse['payload']['robotId'], '-->', sortResponse['payload']['destinationId'])

            # if(IsCamera):
            #     asyncio.run(send_websocket_message(sortResponse, ws_clients[dst_ip]))
            # else:
            #     send_websocket_message(sortResponse, ws_clients[dst_ip])

            print(dst_ip)
            await send_websocket_message(sortResponse, ws_clients[dst_ip])

            induction_bot[k][0] = ''
            induction_bot[k][1] = sortResponse['payload']['robotId'] + '(' + barcode + ')-->' + sortResponse['payload']['destinationId']
            print(induction_bot[k][1])
    else:
        print("Unknown package ID scaned from Camera:", barcode)
        print(package2chute)


def tcp_client(server_host = '127.0.0.1', server_port = 9004):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((server_host, server_port))
                print(f"Connected to TCP server at {server_host}:{server_port}\n")

                client_socket.settimeout(600)
                while True:
                    try:
                        # Attempt to receive data
                        data = client_socket.recv(1024)
                        if not data:  # Connection closed by server
                            print("Connection closed by the server.", server_host, server_port)
                            break
                        data = data.decode()
                        data = re.sub(r"[\x02\r\n\s]", "", data)
                        print(f"Received from {server_host} {server_port}: {data}\n")
                        asyncio.run(src2dst(data, server_host, server_port))

                    except socket.timeout:
                        print("TCP client keeps receiving data")
                        # Optionally handle timeout scenario here, e.g., send a heartbeat message
                    except socket.error as e:
                        print(f"TCP client socket error: {e}")
                        break  # Exit inner loop to reconnect

        except socket.error as e:
            print(f"TCP client error: {server_host} {server_port} {e}")
            # Handle exceptions or reconnect logic here if needed

        client_socket.close()
        print(f"Reconnecting in 1 seconds...")
        time.sleep(1)


def main():
    # while True:
    try:
        # Start HTTP server in a separate thread

        # host = '192.168.0.179'
        host = '192.168.12.116'
        # host = '192.168.137.103'
        port = 8080

        file_3 = open('local_server.txt', 'r')
        server_config = json.loads(file_3.read())

        http_thread = threading.Thread(target=start_http_server, args=(server_config['ip'], server_config['http_port']))
        http_thread.start()

        # Start WebSocket server in a separate thread
        # asyncio.run(start_websocket_server())

        # host = '192.168.12.116'
        port = 9765

        ws_thread = threading.Thread(target=start_websocket_server_in_thread, args=(server_config['ip'], server_config['web_socket_port'], echo))
        ws_thread.start()

        ws_broad = threading.Thread(target=start_websocket_server_in_thread, args=(server_config['ip'], server_config['ws_broad'], broad))
        ws_broad.start()


        # TCP_server_thread = threading.Thread(target=start_TCP_server, args=(server_config['ip'], server_config['tcp_port']))
        # TCP_server_thread.start()
        TCP_server_thread = None

        cam_ips = cams.keys()
        for cam_ip in cam_ips:
            if 'port' in cams[cam_ip]: #Camera works as a TCP server.
                TCP_client_thread = threading.Thread(target=tcp_client, args=(cam_ip, cams[cam_ip]['port']))
                TCP_client_thread.start()
            else: # Camera works as a TCP client.
                if(TCP_server_thread == None):
                    TCP_server_thread = threading.Thread(target=start_TCP_server, args=(server_config['ip'], server_config['tcp_port']))
                    TCP_server_thread.start()

        # Optionally, join threads to wait for completion
        # http_thread.join()
        # tcp_client_thread.join()

        while(True):
            print("Time Stamp: ", time.strftime("%H:%M:%S", time.localtime()))
            time.sleep(10)

    except Exception as e:
        print("Error: ", e)
        # print("Restart Http server, Web socket, and TCP server ")
        # time.sleep(1)

if __name__ == "__main__":
    main()