from fastapi import FastAPI, WebSocket
import uuid

from devices.DeviceManager import DeviceManager
from ws.WebSocketHandler import WebSocketHandler

app = FastAPI()

dm = DeviceManager()
handler = WebSocketHandler(dm)


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    client_id = str(uuid.uuid4())

    try:
        await handler.handle(ws, client_id)
    finally:
        # SAFETY: release everything on disconnect
        dm.release_all_for_client(client_id)