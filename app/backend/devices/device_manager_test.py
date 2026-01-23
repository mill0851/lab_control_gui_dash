from .DeviceManager import DeviceManager
from .DummyScope import DummyScope
from .LabDevice import LabDevice





if __name__ == "__main__":

    # Simple adding devices and retrieving known devices
    device_manager = DeviceManager()
    device_manager.register(DummyScope("test1"))
    device_manager.register(DummyScope("test2"))
    device_manager.register(DummyScope("test3"))    
    print(device_manager.list_devices())
