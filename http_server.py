# HTTP Server
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import jwt

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, this is the HTTP server!")

    def do_POST(self):
        print("do post")

        # Get client IP address
        client_ip, client_port = self.client_address

        # Get server IP address and port
        # server_ip, server_port = self.server.server_address

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
            print("messageNumber info")
        else:
            print("get unknown message:", data)
            pass



def start_http_server():
    host = '192.168.12.116'
    port = 8080

    server = HTTPServer((host, port), MyHTTPRequestHandler)
    print(f"HTTP server listening on {host}:{port}")
    server.serve_forever()

if __name__ == "__main__":
    start_http_server()  # Run this in one terminal
