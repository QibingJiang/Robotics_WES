import asyncio
import threading
import websockets

# Define your WebSocket server coroutine
async def start_websocket_server():
    async with websockets.serve(echo, 'localhost', 8765):  # Replace with your desired host and port
        print("WebSocket server running at ws://localhost:8765")
        await asyncio.Future()  # Run indefinitely

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

# Function to start the WebSocket server in a separate asyncio event loop
def start_websocket_server_in_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_websocket_server())
    loop.run_forever()

# Start WebSocket server in a separate thread
ws_thread = threading.Thread(target=start_websocket_server_in_thread)
ws_thread.start()

# Continue running other code in the main thread
while True:
    # print("Main thread running...")
    # Add your additional main thread logic here
    # time.sleep(1)  # Example of non-blocking operation
