import asyncio
import json
import uuid
import websockets


class LabClient:
    def __init__(self, uri: str):
        self.uri = uri
        self.ws = None
        self.pending = {}

    async def connect(self):
        self.ws = await websockets.connect(self.uri)
        asyncio.create_task(self._listener())

    async def _listener(self):
        async for msg in self.ws:
            data = json.loads(msg)
            future = self.pending.pop(data.get("id"), None)
            if future:
                future.set_result(data)

    async def reserve(self, device_id, duration_s=None):
        await self.ws.send(json.dumps({
            "type": "reserve",
            "device_id": device_id,
            "duration_s": duration_s,
        }))

    async def release(self, device_id):
        await self.ws.send(json.dumps({
            "type": "release",
            "device_id": device_id,
        }))

    async def call(self, device_id, method, *args, **kwargs):
        call_id = str(uuid.uuid4())
        payload = {
            "id": call_id,
            "device_id": device_id,
            "method": method,
            "args": args,
            "kwargs": kwargs,
        }

        fut = asyncio.get_event_loop().create_future()
        self.pending[call_id] = fut
        await self.ws.send(json.dumps(payload))

        response = await fut
        if response["status"] == "error":
            raise RuntimeError(response["error"])

        return response["result"]