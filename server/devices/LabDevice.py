from abc import ABC, abstractmethod
# import sys
# import time
from threading import Lock, Thread

class LabDevice(ABC):
    def __init__(self, device_id: str):
        self.device_id = device_id

    @abstractmethod
    def info(self) -> dict:
        pass  