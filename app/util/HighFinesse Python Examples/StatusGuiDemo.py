######################################################################################################
# @file WlmStatusGuiDemo.py
# @copyright HighFinesse GmbH.
# @version 0.1
#
# Homepage: http://www.highfinesse.com/
#
# This example shows wavelengths, intensities, exposures of all channels and
# allows to set the exposure mode of each channel. A graphical user interface
# (GUI) is made using Tkinter.

from functools import partial
import sys
import tkinter as tk

# wlmData.dll related imports
import wlmConst
import wlmData

def set_exposure_mode(ch):
    """set_exposure_mode is called once an exposure mode checkbox is clicked"""
    dll.SetExposureModeNum(ch + 1, exposure_modes[ch].get())

# Create callback function pointer
@wlmData.CALLBACK_EX_TYPE
def callback_ex(_ver, mode, intval, dblval, _res1):
    """This is called whenever any measurement or state change from the
    wavemeter arrives."""
    wavelength_cmis = [
        wlmConst.cmiWavelength1,
        wlmConst.cmiWavelength2,
        wlmConst.cmiWavelength3,
        wlmConst.cmiWavelength4,
        wlmConst.cmiWavelength5,
        wlmConst.cmiWavelength6,
        wlmConst.cmiWavelength7,
        wlmConst.cmiWavelength8,
    ]
    intensity_cmis = [
        wlmConst.cmiMax11,
        wlmConst.cmiMax12,
        wlmConst.cmiMax13,
        wlmConst.cmiMax14,
        wlmConst.cmiMax15,
        wlmConst.cmiMax16,
        wlmConst.cmiMax17,
        wlmConst.cmiMax18,
    ]
    exposure_cmis = [
        wlmConst.cmiExposureValue11, wlmConst.cmiExposureValue21,
        wlmConst.cmiExposureValue12, wlmConst.cmiExposureValue22,
        wlmConst.cmiExposureValue13, wlmConst.cmiExposureValue23,
        wlmConst.cmiExposureValue14, wlmConst.cmiExposureValue24,
        wlmConst.cmiExposureValue15, wlmConst.cmiExposureValue25,
        wlmConst.cmiExposureValue16, wlmConst.cmiExposureValue26,
        wlmConst.cmiExposureValue17, wlmConst.cmiExposureValue27,
        wlmConst.cmiExposureValue18, wlmConst.cmiExposureValue28,
    ]

    # Update GUI with any received wavelength, intensity or exposure value.
    # Unfortunately, exposure mode updates are only available for the first channel.
    if mode in wavelength_cmis:
        ch = wavelength_cmis.index(mode)
        gui[ch + 1][1].config(text=f'{dblval:.8f}' if dblval > 0 else str(dblval))
    elif mode in intensity_cmis:
        ch = intensity_cmis.index(mode)
        gui[ch + 1][2].config(text=str(intval))
    elif mode in exposure_cmis:
        index = exposure_cmis.index(mode)
        ch = index // 2
        arr = index % 2
        gui[ch + 1][3 + arr].config(text=str(dblval))
    elif mode == wlmConst.cmiExposureMode:
        ch = 0
        exposure_modes[ch].set(bool(intval))

# Load wlmData library. If needed, adjust the path by passing it to LoadDLL()!
try:
    dll = wlmData.LoadDLL()
    #dll = wlmData.LoadDLL('/path/to/your/libwlmData.so')
except OSError as err:
    sys.exit(f'{err}\nPlease check if the wlmData DLL is installed correctly!')

# Create GUI
root = tk.Tk()
root.title('Wavelength meter status')

# Create header row
first_row = [
    tk.Label(root, text='Ch.'),
    tk.Label(root, text='Wavelength'),
    tk.Label(root, text='Pattern 1 max.'),
    tk.Label(root, text='Exposure 1'),
    tk.Label(root, text='Exposure 2+'),
    tk.Label(root, text='Automatic'),
]
gui = [first_row]

# These BooleanVar things are necessary to access exposure mode checkbox state
exposure_modes = [tk.BooleanVar() for ch in range(8)]

# Create GUI elements for each channel
for ch in range(8):
    # Get initial values for current channel using wlmData functions
    wavelength = dll.GetWavelengthNum(ch + 1, 0)
    exposure_mode = dll.GetExposureModeNum(ch + 1, 0)
    pattern_maximum1 = dll.GetAmplitudeNum(ch + 1, wlmConst.cMax1, 0)
    exposure1 = dll.GetExposureNumEx(ch + 1, 1, 0)
    exposure2 = dll.GetExposureNumEx(ch + 1, 2, 0)

    # Create one row of GUI using initial values
    exposure_modes[ch].set(bool(exposure_mode))
    row = [
        tk.Label(root, text=str(ch + 1)),
        tk.Label(root, text=f'{wavelength:.8f}' if wavelength > 0 else str(wavelength)),
        tk.Label(root, text=str(pattern_maximum1)),
        tk.Label(root, text=str(exposure1)),
        tk.Label(root, text=str(exposure2)),
        tk.Checkbutton(root, variable=exposure_modes[ch], command=partial(set_exposure_mode, ch)),
    ]
    gui.append(row)

for i, row in enumerate(gui):
    for j, element in enumerate(row):
        element.grid(row=i, column=j)

# Initialize wlmData callback function for live update of wavelengths
dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyInstallCallbackEx, callback_ex, 0)

# Start measurement
dll.Operation(wlmConst.cCtrlStartMeasurement)

# Run GUI
root.mainloop()

# Cleanup
dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyRemoveCallback, 0, 0)
