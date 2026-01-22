from abc import ABC, abstractmethod
import sys
import time

# ---- dll Imports, change if you modify directories ----
import wlmConst
import wlmData


class Device(abs):
    def __init__(self, name:str):
        # ---- Public ----
        self.name = name

        # ---- Private ----
        self._is_connected = False
        self._is_measuring = False
        self._autostart = False

        @abstractmethod
        def connect(self):
            """Connect Device"""
            pass

        @abstractmethod
        def disconnect(self):
            """Disconnect Device"""
            pass

        @abstractmethod
        def check_connection(self):
            """Check Connection"""
            pass


class WaveMeter(Device):
    def __init__(self, name:str):
        # ---- Load the dll ----
        try:
            self._dll = wlmData.LoadDLL()
        except OSError as err:
            sys.exit(f'{err}\nPlease check if the wlmData DLL is installed correctly!')




        # ---- Inheritance, idk if thats the right word ----
        super().__init__(name)

        # ---- Public ----
        # TODO: Add more features from the documentation, im starting with bare minimum (1/21/26) -Robert


        # ---- Private ----
        # TODO: Add multi channel switch support?
        self._channels = [1]
        self._exposure_mode = "auto"


    # ---- Methods ----
    def connect(self):
        if self._dll.GetWLMCount(0) == 0:
            self._is_connected = False
            print("No Available WLM Server Instances")
            return False
        return None


if __name__ == "__main__":

    wlm = WaveMeter("WaveMeter")
    print(f"Exposure mode: {wlm.get_exposure_mode()}")






