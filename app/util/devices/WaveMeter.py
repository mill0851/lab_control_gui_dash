# ---- dll Imports, change if you modify directories ----
import wlmConst
import wlmData

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
        # TODO: Add more features from the documentation


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
