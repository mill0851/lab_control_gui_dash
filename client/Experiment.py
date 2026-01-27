class Experiment:
    def __init__(self, client):
        self.client = client
        self.devices = []

    async def __aenter__(self):
        return self

    async def reserve(self, device_id, duration_s=None):
        await self.client.reserve(device_id, duration_s)
        self.devices.append(device_id)

    async def __aexit__(self, exc_type, exc, tb):
        # GUARANTEED CLEANUP PATH
        for device_id in self.devices:
            try:
                await self.client.release(device_id)
            except Exception:
                pass