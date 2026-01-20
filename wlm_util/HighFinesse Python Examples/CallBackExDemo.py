######################################################################################################
# @file CallBackDemo.py
# @copyright HighFinesse GmbH.
# @author Lovas Szilard <lovas@highfinesse.de>
# @date 2018.09.16
# @version 0.1
#
# Homepage: http://www.highfinesse.com/
#
# @brief Python language example for demonstrating usage of wlmData.dll CallBack mechanism.
# Tested with Python 3.7.
# 64-bit Python requires 64-bit wlmData.dll (in System32 folder) and
# 32-bit Python requires 32-bit wlmData.dll (in SysWOW64 folder on Win64 or System32 folder on Win32).
# For more information see the ctypes module documentation:
# https://docs.python.org/3/library/ctypes.html
# and/or WLM manual.pdf
#
# Changelog:
# ----------
# 2018.09.16
# v0.1 - Initial release
#

import sys
import time

# wlmData.dll related imports
import wlmConst
import wlmData

# Set the Data acquisition time (sec) here:
DATA_ACQUISITION_TIME = 1

# Set the CallBack Thread priority here:
CALLBACK_THREAD_PRIORITY = 2

# Create callback function pointer
@wlmData.CALLBACK_EX_TYPE
def my_callback_ex(ver, mode, _intval, dblval, _res1):
    """This wlmData callback function prints the wavemeter serial number
    alongside received wavelength results"""
    print(f'Device {ver}', end=', ')
    if mode == wlmConst.cmiWavelength1:
        print(f'Ch1 wavelength (vac): {dblval} nm')
    elif mode == wlmConst.cmiLinewidth1:
        print(f'Ch1 linewidth (vac): {dblval} nm')
    elif mode == wlmConst.cmiWavelength2:
        print(f'Ch2 wavelength (vac): {dblval} nm')
    elif mode == wlmConst.cmiWavelength3:
        print(f'Ch3 wavelength (vac): {dblval} nm')
    elif mode == wlmConst.cmiWavelength4:
        print(f'Ch4 wavelength (vac): {dblval} nm')

# Load wlmData library. If needed, adjust the path by passing it to LoadDLL()!
try:
    dll = wlmData.LoadDLL()
    #dll = wlmData.LoadDLL('/path/to/your/libwlmData.so')
except OSError as err:
    sys.exit(f'{err}\nPlease check if the wlmData DLL is installed correctly!')

# Check the number of WLM server instances
if dll.GetWLMCount(0) == 0:
    sys.exit('There is no running WLM server instance.')

print(f'Data acquisition by callback function for {DATA_ACQUISITION_TIME} seconds.')

# Install callback function
dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyInstallCallbackEx, my_callback_ex,
    CALLBACK_THREAD_PRIORITY)

for i in range(dll.GetWLMCount(0)):
    dll.PresetWLMIndex(i)
    dll.SetLinewidthMode(True)

# Give a little time for data acquisition
time.sleep(DATA_ACQUISITION_TIME)

# Remove callback function
dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyRemoveCallback, None, 0)

print('Callback function was removed.')
