from abc import ABC, abstractmethod
import sys
import time
from threading import Lock, Thread

class Device(ABC):
    def __init__(self, device_id: str):
        self.device_id = device_id
        self.lock = Lock()
        self.status = "idle"

    def acquire(self):
        acquired = self.lock.acquire(blocking=False)
        if acquired:
            self.status = "busy"
        return acquired

    def release(self):
        self.status = "idle"
        self.lock.release()

    @abstractmethod
    def info(self) -> dict:
        pass  