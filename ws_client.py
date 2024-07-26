import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print(websocket)
        await websocket.send("This is client 1.")
        response = await websocket.recv()
        print(f"Received from server: {response}")

asyncio.run(hello())
