from .LabDevice import LabDevice
import time
import numpy as np
import random

class DummyScope(LabDevice):
    def __init__(self, device_id: str, channel: int = 1, volt_div: int = 1):
        super().__init__(device_id)
        self.channel = channel
        self.volt_div = volt_div

    def info(self):
        return {
            "id": self.device_id,
            "type": "DummyScope",
            "status": self.status,
            "capabilities": ["get_voltage",
                             "get_channel",
                             "set_channel",
                             "volt_longterm"]
        }
    
    def get_voltage(self) -> dict:
        voltage = random.randint(1,100)
        return {"voltage": voltage}
    
    def get_channel(self) -> dict:
        return {"channel": self.channel}
    
    def set_channel(self, channel: int = 1) -> dict:
        self.channel = channel

    def volt_longterm(self, channel, duration) -> dict:
        t = []
        data = []
        start = time.time()

        while time.time() - start < duration:
            t.append(time.time())
            data.append(np.sin(2*np.pi*(1/0.01)*t))
            time.sleep(0.0005)
        
        return {"voltage": data, "time": t}

