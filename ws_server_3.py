# server.py
import asyncio
import time

import websockets
import threading
import sys

clients = set()

async def handler(websocket, path):
    clients.add(websocket)

async def main():
    # async with websockets.serve(handler, "localhost", 8080):
    async with websockets.serve(handler, "192.168.12.116", 10253):
        await asyncio.Future()

def start_server():
    asyncio.run(main())


if __name__ == "__main__":

    threading.Thread(target=start_server, daemon=True).start()

    while True:
        message = "Hello"
        for client in clients:
            asyncio.run(client.send(message))

        time.sleep(0.5)

