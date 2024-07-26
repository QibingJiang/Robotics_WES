# HTTP Client
import http.client
import json
import jwt

def start_http_client():
    # conn = http.client.HTTPConnection('127.0.0.1', 8080)
    # conn.request('GET', '/')

    data = {
        "name": "Upendra",
        "job": "Programmer"
    }
    json_input_string = json.dumps(data)

    conn = http.client.HTTPConnection('127.0.0.1', 8080)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    conn.request("POST", "/api/users", json_input_string, headers)


    response = conn.getresponse()

    data_str = response.read().decode()
    print(f"Received from server: {data_str}")

    data_json = json.loads(data_str)


    jwt_recv = data_json['token']

    SECRET_KEY = "my-secret-key"

    decoded_payload = jwt.decode(jwt_recv, SECRET_KEY, algorithms=["HS512"])

    print(f"Decoded Payload: {decoded_payload}")

    conn.close()

if __name__ == "__main__":
    start_http_client()  # Uncomment and run this in another terminal
