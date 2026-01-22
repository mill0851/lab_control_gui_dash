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

# wlmData.dll related imports
import wlmData
import wlmConst

# others
import sys

#########################################################
# Set the DLL_PATH variable according to your environment
#########################################################
DLL_PATH = "wlmData.dll"


# Load DLL from DLL_PATH
try:
    wlmData.LoadDLL(DLL_PATH)
except:
    sys.exit("Error: Couldn't find DLL on path %s. Please check the DLL_PATH variable!" % DLL_PATH)

# Checks the number of WLM server instance(s)
if wlmData.dll.GetWLMCount(0) == 0:
    print("There is no running wlmServer instance(s).")
else:
    #Set Switch mode
    wlmData.dll.SetSwitcherMode(1)
    #Set the Use and Shows checkbox for any individual channel     
    wlmData.dll.SetSwitcherSignalStates(2,1,0) #sets channel 2 to be used but the pattern will not be displayed. Will be updated as soon as a measurement arrives. 


    
    



