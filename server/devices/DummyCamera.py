from .LabDevice import LabDevice
import time
import numpy as np
import random

class DummyCamera(LabDevice):
    def info(self):
        return {
            "type": "camera",
            "id": self.device_id
        }

    def capture(self):
        print(f"Getting Picture {self.device_id}")
        time.sleep(0.2)
        return f"IMAGE {self.device_id}"