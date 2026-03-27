# main.py
import os
import json
from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    # Render health check (HEAD/GET) won’t crash the server
    return {"status": "ok"}

@app.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    print("Client connected")

    try:
        # Step 1: Handshake
        data = await ws.receive_text()
        print("Handshake received:", data)

        msg = json.loads(data)
        if msg.get("type") == "hello":
            response = {
                "type": "welcome",
                "status": "ok",
                "version": msg.get("version"),
                "player": {
                    "username": msg.get("username"),
                    "id": msg.get("profileId")
                }
            }

            # Send welcome message
            await ws.send_text(json.dumps(response))

            # Optional: tell client we are ready
            await ws.send_text(json.dumps({"type": "ready"}))

        # Step 2: Keep connection alive
        while True:
            msg = await ws.receive_text()
            print("Received:", msg)

            # For now, echo messages back (stub multiplayer)
            await ws.send_text(json.dumps({"type": "ack", "data": msg}))

    except Exception as e:
        print("Client disconnected or error:", e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
