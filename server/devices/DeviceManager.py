from datetime import datetime, timedelta
from typing import Dict
from .DummyCamera import DummyCamera
from .LabDevice import LabDevice
from .DeviceLease import DeviceLease


MAX_LEASE_SECONDS = 3600  # hard safety cap


class DeviceManager:
    def __init__(self):
        self.devices: Dict[str, LabDevice] = {
            "cam1": DummyCamera("cam1"),
            "cam2": DummyCamera("cam2"),
        }
        self.leases: Dict[str, DeviceLease] = {}


    def reserve(self, device_id: str, client_id: str, duration_s: int | None):

        self._cleanup()
        if device_id in self.leases:
            raise RuntimeError("Device already reserved")

        if duration_s is not None:
            duration_s = min(duration_s, MAX_LEASE_SECONDS)
            expires_at = datetime.utcnow() + timedelta(seconds=duration_s)
        else:
            expires_at = None

        self.leases[device_id] = DeviceLease(
            device_id=device_id,
            client_id=client_id,
            expires_at=expires_at,
        )

    def release(self, device_id: str, client_id: str):
        lease = self.leases.get(device_id)
        if not lease or lease.client_id != client_id:
            raise RuntimeError("Cannot release device")
        del self.leases[device_id]

    def release_all_for_client(self, client_id: str):
        for device_id, lease in list(self.leases.items()):
            if lease.client_id == client_id:
                del self.leases[device_id]

    def get_device(self, device_id: str, client_id: str) -> LabDevice:
        self._cleanup()
        lease = self.leases.get(device_id)

        if not lease or lease.client_id != client_id:
            raise RuntimeError("Device not reserved")

        return self.devices[device_id]

    def _cleanup(self):
        for device_id, lease in list(self.leases.items()):
            if lease.expired():
                del self.leases[device_id]
