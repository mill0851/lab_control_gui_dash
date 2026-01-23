from .DummyScope import DummyScope
from .LabDevice import LabDevice

class DeviceManager:
    def __init__(self):
        self.devices = {}
    
    def register(self, device):
        self.devices[device.device_id] = device
    
    def list_devices(self):
        return [d.info() for d in self.devices.values()]
    
    def get(self, device_id):
        return self.devices[device_id]
