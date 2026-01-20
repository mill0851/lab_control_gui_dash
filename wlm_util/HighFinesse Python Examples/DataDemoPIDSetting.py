######################################################################################################
# @file DataDemo.py
# @copyright HighFinesse GmbH.
# @author Lovas Szilard <lovas@highfinesse.de>
# @date 2018.09.15
# @version 0.1
#
# Homepage: http://www.highfinesse.com/
#
# @brief Python language example for demonstrating usage of
# wlmData.dll Set/Get function calls.
# Tested with Python 3.7. 64-bit Python requires 64-bit wlmData.dll and
# 32-bit Python requires 32-bit wlmData.dll.
# For more information see ctypes module documentation:
# https://docs.python.org/3/library/ctypes.html
# and/or WLM manual.pdf
#
# Changelog:
# ----------
# 2018.09.15
# v0.1 - Initial release
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

# Check the number of WLM server instances
if dll.GetWLMCount(0) == 0:
    sys.exit('There is no running WLM server instance.')

# Read type, version, revision and build number
version_type = dll.GetWLMVersion(0)
version_ver = dll.GetWLMVersion(1)
version_rev = dll.GetWLMVersion(2)
version_build = dll.GetWLMVersion(3)
print(f'WLM version: [{version_type}.{version_ver}.{version_rev}.{version_build}]')
#wlmData.dll.Operation(wlmConst.cCtrlStartMeasurement)

# Get PID settings (intval and doubleval will have the values)
intval = ctypes.c_int32(0)
doubleval = ctypes.c_double(0)
dll.GetPIDSetting(wlmConst.cmiPID_P, 1, intval, doubleval)

# Set PID parameter D to 0.006
#dll.SetPIDSetting(wlmConst.cmiPID_D, 1, intval, 0.006)

#Get PID reference/target
course = (ctypes.c_char * 1024)()
wlmData.dll.GetPIDCourseNum(1, course)
print('Target wavelength channel 1 ' + course.value.decode())

# Set PID reference/target
# Watch out to use the correct delimiter for your country "." or ","
#course2 = b'=800-0,001triangle(t)\0'
#dll.SetPIDCourseNum(1, ctypes.cast(course2, ctypes.POINTER(ctypes.c_char)))

# Activate PID Regulation
#dll.SetDeviationMode(1) # activate 1 or deactivate 0 regulation
