import json
from devices.DeviceManager import DeviceManager
from starlette.websockets import WebSocketDisconnect


class WebSocketHandler:
    def __init__(self, dm: DeviceManager):
        self.dm = dm

    async def handle(self, ws, client_id: str):
        try:
            while True:
                msg = json.loads(await ws.receive_text())
                msg_type = msg.get("type", "call")

                try:
                    if msg_type == "reserve":
                        self.dm.reserve(
                            msg["device_id"],
                            client_id,
                            msg.get("duration_s"),
                        )
                        await ws.send_text(json.dumps({"status": "ok"}))
                        continue

                    if msg_type == "release":
                        self.dm.release(msg["device_id"], client_id)
                        await ws.send_text(json.dumps({"status": "ok"}))
                        continue

                    # method call
                    device = self.dm.get_device(msg["device_id"], client_id)
                    method = getattr(device, msg["method"])
                    result = method(*msg["args"], **msg["kwargs"])

                    await ws.send_text(json.dumps({
                        "id": msg["id"],
                        "status": "ok",
                        "result": result,
                    }))

                except Exception as e:
                    await ws.send_text(json.dumps({
                        "id": msg.get("id"),
                        "status": "error",
                        "error": str(e),
                    }))
        except WebSocketDisconnect:
            print(f"Client {client_id} disconnected")
        except json.JSONDecodeError:
            print(f"Client {client_id} sent invalid JSON")