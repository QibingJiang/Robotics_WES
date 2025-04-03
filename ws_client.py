import asyncio
import websockets

async def hello():
    # uri = "ws://localhost:8765"
    uri = "ws://192.168.12.116:10253"
    async with websockets.connect(uri) as websocket:
        print(websocket)
        async for message in websocket:
            print(f"Received from server: {message}")

asyncio.run(hello())
