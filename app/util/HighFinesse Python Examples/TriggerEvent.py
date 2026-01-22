######################################################################################################
# @file AnalysisDataDemo.py
# @copyright HighFinesse GmbH.
# @version 0.1
#
# Homepage: http://www.highfinesse.com/
#

import ctypes
import sys

# wlmData.dll related imports
import wlmConst
import wlmData

# Load wlmData library. If needed, adjust the path by passing it to LoadDLL()!
try:
    dll = wlmData.LoadDLL()
    #dll = wlmData.LoadDLL('/path/to/your/libwlmData.so')
except OSError as err:
    sys.exit(f'{err}\nPlease check if the wlmData DLL is installed correctly!')

# Set up WaitForWLMEvent mechanism
ret = dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyInstallWaitEventEx, -1, 0)
if ret <= 0:
    sys.exit(f'Instantiate failed returning {ret}')

while True:
    input('Press enter to trigger a measurement')

    # Call TriggerMeasurement twice to ascertain that a new sensor readout is started.
    for i in range(2):
        dll.ClearWLMEvents()
        dll.TriggerMeasurement(wlmConst.cCtrlMeasurementTriggerSuccess)
        # Fetch data from WLM/LSA until the triggered measurement has been received.
        while True:
            ver = ctypes.c_int32()
            mode = ctypes.c_int32()
            intval = ctypes.c_int32()
            dblval = ctypes.c_double()
            res1 = ctypes.c_int32()
            ret = dll.WaitForWLMEventEx(ver, mode, intval, dblval, res1)
            if ret <= 0:
                continue
            if mode.value == wlmConst.cmiWavelength1:
                wavelength = dblval.value
            elif mode.value == wlmConst.cmiTriggerState:
                if intval.value == wlmConst.cCtrlMeasurementTriggerSuccess:
                    break
    print(wavelength)
