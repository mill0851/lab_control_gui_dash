"""
NetAccess API constants generated from wlmDataNetworkConstants.h on 2024-11-12
"""
# pylint: disable=invalid-name

# Server access return (FAccess) constants



# Instantiate() function network library specific parameters

# Log and error callback control: 'RFC' = cInstNotification
# =========================================================
# Log and error 'Mode' constants:
cNotifyInstallLogEvent = 1000
cNotifyInstallErrorEvent = 1001
cNotifyRemoveLogEvent = 1002
cNotifyRemoveErrorEvent = 1003

# Network connection control 'RFC' = cInstNetworkControl
# ======================================================

cInstNetworkControl = 6

# Network connection control 'Mode' constants
cSetConnectState = 1000
cGetConnectState = 1001
cSetParameter = 1002
cGetParameter = 1003

# Network connection states


# Error Source IDs others:
cCallbackServer = -1

# Error Source IDs API functions
# Functions for general usage
cInstantiate = 0

cCallbackProc = 1
cCallbackProcEx = 2

cWaitForWLMEvent = 3
cWaitForWLMEventEx = 4
cWaitForNextWLMEvent = 5
cWaitForNextWLMEventEx = 6
cClearWLMEvents = 7

cControlWLM = 8
cControlWLMEx = 9
cSynchroniseWLM = 10
cSetMeasurementDelayMethod = 11
cSetWLMPriority = 12
cPresetWLMIndex = 13

cGetWLMVersion = 14
cGetWLMIndex = 15
cGetWLMCount = 16

# General Get... & Set...-functions
cGetWavelength = 17
cGetWavelength2 = 18
cGetWavelengthNum = 19
cGetCalWavelength = 20
cGetCalibrationEffect = 21
cGetFrequency = 22
cGetFrequency2 = 23
cGetFrequencyNum = 24
cGetLinewidth = 25
cGetLinewidthNum = 26
cGetDistance = 27
cGetAnalogIn = 28
cGetTemperature = 29
cSetTemperature = 30
cGetPressure = 31
cSetPressure = 32
cGetExternalInput = 33
cSetExternalInput = 34
cGetExtraSetting = 35
cSetExtraSetting = 36

cGetExposure = 37
cSetExposure = 38
cGetExposure2 = 39
cSetExposure2 = 40
cGetExposureNum = 41
cSetExposureNum = 42
cGetExposureNumEx = 43
cSetExposureNumEx = 44
cGetExposureMode = 45
cSetExposureMode = 46
cGetExposureModeNum = 47
cSetExposureModeNum = 48
cGetExposureRange = 49
cGetAutoExposureSetting = 50
cSetAutoExposureSetting = 51

cGetResultMode = 52
cSetResultMode = 53
cGetRange = 54
cSetRange = 55
cGetPulseMode = 56
cSetPulseMode = 57
cGetPulseDelay = 58
cSetPulseDelay = 59
cGetWideMode = 60
cSetWideMode = 61

cGetDisplayMode = 62
cSetDisplayMode = 63
cGetFastMode = 64
cSetFastMode = 65

cGetLinewidthMode = 66
cSetLinewidthMode = 67

cGetDistanceMode = 68
cSetDistanceMode = 69

cGetSwitcherMode = 70
cSetSwitcherMode = 71
cGetSwitcherChannel = 72
cSetSwitcherChannel = 73
cGetSwitcherSignalStates = 74
cSetSwitcherSignalStates = 75
cSetSwitcherSignal = 76

cGetAutoCalMode = 77
cSetAutoCalMode = 78
cGetAutoCalSetting = 79
cSetAutoCalSetting = 80

cGetActiveChannel = 81
cSetActiveChannel = 82
cGetChannelsCount = 83

cGetOperationState = 84
cOperation = 85
cSetOperationFile = 86
cCalibration = 87
cRaiseMeasurementEvent = 88
cTriggerMeasurement = 89
cGetTriggerState = 90
cGetInterval = 91
cSetInterval = 92
cGetIntervalMode = 93
cSetIntervalMode = 94
cGetBackground = 95
cSetBackground = 96
cGetAveragingSettingNum = 97
cSetAveragingSettingNum = 98

cGetLinkState = 99
cSetLinkState = 100
cLinkSettingsDlg = 101

cGetPatternItemSize = 102
cGetPatternItemCount = 103
cGetPattern = 104
cGetPatternNum = 105
cGetPatternData = 106
cGetPatternDataNum = 107
cSetPattern = 108
cSetPatternData = 109

cGetAnalysisMode = 110
cSetAnalysisMode = 111
cGetAnalysisItemSize = 112
cGetAnalysisItemCount = 113
cGetAnalysis = 114
cGetAnalysisData = 115
cSetAnalysis = 116

cGetMinPeak = 117
cGetMinPeak2 = 118
cGetMaxPeak = 119
cGetMaxPeak2 = 120
cGetAvgPeak = 121
cGetAvgPeak2 = 122
cSetAvgPeak = 123

cGetAmplitudeNum = 124
cGetIntensityNum = 125
cGetPowerNum = 126

cGetDelay = 127
cSetDelay = 128
cGetShift = 129
cSetShift = 130
cGetShift2 = 131
cSetShift2 = 132

# Deviation and PID-functions
cGetDeviationMode = 133
cSetDeviationMode = 134
cGetDeviationReference = 135
cSetDeviationReference = 136
cGetDeviationSensitivity = 137
cSetDeviationSensitivity = 138
cGetDeviationSignal = 139
cGetDeviationSignalNum = 140
cSetDeviationSignal = 141
cSetDeviationSignalNum = 142
cRaiseDeviationSignal = 143

cGetPIDCourse = 144
cSetPIDCourse = 145
cGetPIDCourseNum = 146
cSetPIDCourseNum = 147
cGetPIDSetting = 148
cSetPIDSetting = 149
cGetLaserControlSetting = 150
cSetLaserControlSetting = 151
cClearPIDHistory = 152

# Other...-functions
cConvertUnit = 153
cConvertDeltaUnit = 154

# Obsolete...-functions
cGetReduced = 155
cSetReduced = 156
cGetScale = 157
cSetScale = 158

# FID range 159-163 reserved for internal usage

cGetAirParameters = 164
cSetAirParameters = 165
cGetExposureRangeEx = 166

# API level 7.254.xx level function IDs
#const int32_t cGetOptionInfo = 167;			// Obsolote function signature, compared to 7.263.xx
cGetInternalTriggerRate = 168
cSetInternalTriggerRate = 169
cGetGain = 170
cSetGain = 171
cGetMultimodeInfo = 172

# API level 7.263.xx level function IDs
cGetWLMInfo = 173
cGetDeviceInfo = 174
cGetOptionInfo = 175 # Updated function signature, compared to 7.254.xx
cGetResultInfo = 176
cGetPulseIntegration = 177
cSetPulseIntegration = 178
cPowerCalibration = 179 # (set function)
