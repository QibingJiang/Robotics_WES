# client.py
import asyncio
import websockets

async def listen_for_messages(websocket):
    async for message in websocket:
        print(f"Received from server: {message}")

async def main():
    uri = "ws://192.168.12.116:8765"
    async with websockets.connect(uri) as websocket:
        print("Connected to the server")

        # Start listening for messages from the server in the background
        asyncio.create_task(listen_for_messages(websocket))

        # Keep the client running to continuously receive messages
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
