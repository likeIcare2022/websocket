# main.py
import os
import json
from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    # Render health check
    return {"status": "ok"}

@app.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    print("Client connected")

    try:
        # Step 1: Wait for handshake
        data = await ws.receive_text()
        print("Handshake received:", data)

        msg = json.loads(data)
        if msg.get("type") == "hello":
            # Respond with welcome
            response = {
                "type": "welcome",
                "status": "ok",
                "version": msg.get("version"),
                "player": {
                    "username": msg.get("username"),
                    "id": msg.get("profileId")
                }
            }
            await ws.send_text(json.dumps(response))

            # Optional: mark ready
            await ws.send_text(json.dumps({"type": "ready"}))

        # Step 2: Keep connection alive and catch errors
        while True:
            try:
                msg = await ws.receive_text()
                print("Received:", msg)

                # Echo back (stub)
                await ws.send_text(json.dumps({"type": "ack", "data": msg}))

            except Exception as e_inner:
                print("Error during message handling:", e_inner)
                continue  # don’t close the socket

    except Exception as e:
        print("Socket closed or handshake failed:", e)
        # Do not re-raise, just log

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
