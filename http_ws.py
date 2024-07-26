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

file_1 = open('cam_config.txt', 'r')
cam_config = file_1.read()
cams = json.loads(cam_config)

ip_cam = {}
induction_cam = {}

for cam in cams["cams"]:
    ip_cam[cam["camIP"]] = cam

    keys = list(cam.keys())
    for i in range(2, len(keys)):
        key = keys[i]
        cam[key].append('')
        induction_cam[(key, cam[key][0])] = cam


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
        print("Http server get post")

        # Get client IP address
        client_ip, client_port = self.client_address

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)

        print(data)

        if('username' in data):

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
             "exp": 1735195000
            }

            # Encode the payload into a JWT
            encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS512")
            print(f"Encoded JWT: {encoded_jwt}")

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

                cam = induction_cam[(client_ip, data['currentLocationId'])]
                assert cam[client_ip][0] == data['currentLocationId']
                cam[client_ip][1] = data['robotId']

        else:
            print("get unknown message:", data)
            pass

def start_http_server(host, port):

    server = HTTPServer((host, port), MyHTTPRequestHandler)
    print(f"HTTP server listening on {host}:{port}")
    server.serve_forever()

async def echo(websocket):
    print("one websocket get connected.", websocket)

    client_ip = websocket.remote_address[0]
    if(client_ip == '::1'):
        client_ip = '127.0.0.1'

    ws_clients[client_ip] = websocket
    print(f"Websocket Client {client_ip} connected.")

    async for message in websocket:
        print(message)
        await websocket.send(message)

async def start_websocket_server(IP, port):
    async with websockets.serve(echo, IP, port) as ws_sever:
        print("Web socket server ", IP, "listening at ", port)
        await asyncio.Future()  # Run forever

# Function to start the WebSocket server in a separate asyncio event loop
def start_websocket_server_in_thread(IP, port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_websocket_server(IP, port))
    loop.run_forever()

async def send_websocket_message(message, websocket):
    try:
        await websocket.send(json.dumps(message).encode())
    except Exception as e:
        print(f"Failed to send message: {e}")


def tcp_client(server_host = '127.0.0.1', server_port = 9004):
    while True:
        # try:
            # Connect to TCP server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((server_host, server_port))
                print(f"Connected to TCP server at {server_host}:{server_port}\n")

                client_socket.settimeout(None)
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        print("TCP break ", "server_host ", "server_port ")
                        break
                        # time.sleep(1)
                        # continue
                    data = data.decode()
                    print(f"Received from {server_host} {server_port}: {data}\n")

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

                    dst_ip = package2chute[data][0]

                    cam = ip_cam[server_host]
                    sortResponse['payload']['stationId'] = cam[dst_ip][0]

                    if(len(cam[dst_ip]) < 2 or cam[dst_ip][1] == ''):
                        print("No robot at induction: ", dst_ip, cam[dst_ip][0])
                        continue

                    sortResponse['payload']['robotId'] = cam[dst_ip][1]
                    if(mode == 'sort'):
                        sortResponse['payload']['destinationId'] = package2chute[data][1]
                    else:
                        sortResponse['payload']['destinationId'] = random.choice(IP2chutes[dst_ip])

                    print(sortResponse)

                    asyncio.run(send_websocket_message(sortResponse, ws_clients[dst_ip]))


        # except Exception as e:
        #     print(f"Error: {server_host} {server_port} {e}")
        #     # Handle exceptions or reconnect logic here if needed


def main():
    # Start HTTP server in a separate thread

    host = '192.168.12.116'
    port = 8080

    http_thread = threading.Thread(target=start_http_server, args=(host, port))
    http_thread.start()

    # Start WebSocket server in a separate thread
    # asyncio.run(start_websocket_server())

    host = '192.168.12.116'
    port = 9765

    ws_thread = threading.Thread(target=start_websocket_server_in_thread, args=(host, port))
    ws_thread.start()

    # Start TCP clients in a separate thread
    for i in range(len(cams["cams"]) - 1):
        tcp_client_thread = threading.Thread(target=tcp_client, args=(cams["cams"][i]["camIP"], cams["cams"][i]["port"]))
        tcp_client_thread.start()

    tcp_client(cams["cams"][-1]["camIP"], cams["cams"][-1]["port"])

    # Optionally, join threads to wait for completion
    # http_thread.join()
    # tcp_client_thread.join()

if __name__ == "__main__":
    main()