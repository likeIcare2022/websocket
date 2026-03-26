import asyncio
import websockets
import os

PORT = int(os.environ.get("PORT", 10000))

async def handler(websocket):
    print("Client connected")

    try:
        async for message in websocket:
            print("Received:", message)

            # Temporary: respond so client doesn't crash
            await websocket.send('{"status":"ok"}')

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"Running on port {PORT}")
        await asyncio.Future()

asyncio.run(main())
