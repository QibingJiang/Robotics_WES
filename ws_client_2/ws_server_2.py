# server.py
import asyncio
import websockets
import threading
import sys

clients = set()

async def handler(websocket, path):
    clients.add(websocket)
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Received message from client: {message}")
    except websockets.ConnectionClosed:
        print("Client disconnected")
    finally:
        clients.remove(websocket)

async def main(ip, port):
    # ip = "192.168.12.116"
    # port = 8765
    async with websockets.serve(handler, ip, port):
        print("WebSocket server is running on ws://" + ip + ":" + str(port))
        await asyncio.Future()  # run forever

def start_server(ip, port):
    asyncio.run(main(ip, port))

def send_message():
    while True:
        message = input("Server: ")
        if message:
            # Send message to all connected clients
            for client in clients:
                asyncio.run(client.send(message))

if __name__ == "__main__":
    sys.argv[1:], sys.argv[2:]
    # Start the WebSocket server in a separate thread
    threading.Thread(target=start_server, args=(sys.argv[1], sys.argv[2]), daemon=True).start()
    # Start sending messages from the keyboard
    send_message()
