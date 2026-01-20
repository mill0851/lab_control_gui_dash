######################################################################################################
# @file AnalysisDataDemo.py
# @copyright HighFinesse GmbH.
# @version 0.1
#
# Homepage: http://www.highfinesse.com/
#

import sys
import ctypes

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# wlmData.dll related imports
import wlmConst
import wlmData

# Load wlmData library. If needed, adjust the path by passing it to LoadDLL()!
try:
    dll = wlmData.LoadDLL()
    #dll = wlmData.LoadDLL('/path/to/your/libwlmData.so')
except OSError as err:
    sys.exit(f'{err}\nPlease check if the wlmData DLL is installed correctly!')

# Checks the number of LSA server instances
if dll.GetWLMCount(0) == 0:
    sys.exit('There is no running LSA server instance.')

# Enable analysis mode
dll.SetAnalysisMode(True)

# Enable analysis data export
dll.SetAnalysis(wlmConst.cSignalAnalysis, wlmConst.cAnalysisEnable)

# Set up WaitForWLMEvent mechanism
ret = dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyInstallWaitEventEx, -1, 0)
if ret <= 0:
    sys.exit(f'Instantiate failed returning {ret}')

# Fetch live data from LSA
ver = ctypes.c_int32()
mode = ctypes.c_int32()
intval = ctypes.c_int32()
dblval = ctypes.c_double()
res1 = ctypes.c_int32()

print('Waiting for analysis data')

parameters_requested = False

while True:
    ret = dll.WaitForWLMEventEx(ver, mode, intval, dblval, res1)
    if ret <= 0:
        continue

    if mode.value == wlmConst.cmiPatternAnalysisWritten:
        if not parameters_requested:
            # Request analysis data parameters (these don't change later).
            analysis_item_size = dll.GetAnalysisItemSize(wlmConst.cSignalAnalysis)
            analysis_item_count = dll.GetAnalysisItemCount(wlmConst.cSignalAnalysis)

            if analysis_item_size == 4:
                analysis_array = ctypes.c_float * analysis_item_count
            elif analysis_item_size == 8:
                analysis_array = ctypes.c_double * analysis_item_count
            else:
                sys.exit(f'Unknown analysis item size {analysis_item_size}')

            analysis_x = analysis_array()
            analysis_y = analysis_array()

            parameters_requested = True

        # Request analysis data
        dll.GetAnalysisData(wlmConst.cSignalAnalysisX, analysis_x)
        dll.GetAnalysisData(wlmConst.cSignalAnalysisY, analysis_y)

        npanalysis_x = np.array(analysis_x)
        npanalysis_y = np.array(analysis_y)
        peak_ind, _ = find_peaks(npanalysis_y, 0.1)

        # Update plot
        plt.clf()
        plt.subplot(2, 1, 1)
        plt.plot(npanalysis_x, npanalysis_y)
        plt.plot(npanalysis_x[peak_ind], npanalysis_y[peak_ind], 'x')
        plt.pause(.001)
