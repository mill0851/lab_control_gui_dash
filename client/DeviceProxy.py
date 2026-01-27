
class DeviceProxy:
    def __init__(self, client, device_id):
        self._client = client
        self._device_id = device_id

    def __getattr__(self, name):
        async def method(*args, **kwargs):
            return await self._client.call(
                self._device_id, name, *args, **kwargs
            )
        return method
