import asyncio
import websockets

clients = {}

async def echo(websocket):
    print("one websocket get connected.", websocket)

    client_ip = websocket.remote_address[0]
    clients[client_ip] = websocket
    print(f"Client {client_ip} connected.")

    async for message in websocket:
        print(message)
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "localhost", 8765) as ws_sever:
        print(ws_sever)
        await asyncio.Future()  # Run forever

asyncio.run(main())
