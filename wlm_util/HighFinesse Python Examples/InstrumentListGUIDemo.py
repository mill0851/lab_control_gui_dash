######################################################################################################
# @file DeviceListGuiDemo.py
# @copyright HighFinesse GmbH.
# @version 0.1
#
# Homepage: http://www.highfinesse.com/
#
# This example shows a list of connected wavelength meters along with live
# wavelengths in a Tkinter graphical user interface (GUI).

import sys
from dataclasses import dataclass
import tkinter as tk

# wlmData.dll related imports
import wlmConst
import wlmData

@dataclass
class Instrument:
    """Data for each available measurement instrument"""
    button: tk.Button
    info: str
    wavelengths: dict[int, float]

# For each measurement instrument that is found, store an Instrument object in
# this dictionary
instruments = {}

def refresh():
    """Clear and rebuild GUI based on found instruments. Called once at startup
    and each time the refresh button is clicked."""
    # Clear instrument list
    for instrument in instruments.values():
        instrument.button.destroy()
    instruments.clear()

    # Check instrument count
    wlm_count = dll.GetWLMCount(0)
    if wlm_count == 0:
        refresh_button.config(text='Could not find any instruments. Click to refresh')
        return
    refresh_button.config(text='Refresh')

    # Iterate over instruments. For each instrument that is found: Retrieve type
    # and serial number, create a tk.Button and store an Instrument object for
    # later retrieval in "instruments" dictionary.
    i = 0
    while True:
        dll.PresetWLMIndex(i)
        instrument_type = dll.GetWLMVersion(0)
        serial = dll.GetWLMVersion(1)
        if serial not in instruments:
            instrument_name = 'WLM/LSA' if instrument_type == 5 else 'WLM'
            info = f'{instrument_name} {serial}'
            button = tk.Button(root, text=info)
            button.pack()
            instruments[serial] = Instrument(button=button, info=info, wavelengths={})
            if len(instruments) == wlm_count:
                break
        i += 1

# Create callback function pointer
@wlmData.CALLBACK_EX_TYPE
def callback_ex(ver, mode, _intval, dblval, _res1):
    """Update shown wavelengths in the GUI"""
    # Use the serial number to retrieve the instrument from the dictionary
    try:
        instrument = instruments[ver]
    except KeyError:
        return

    # If any wavelength was received...
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
    if mode in wavelength_cmis:
        # ...store it...
        channel = wavelength_cmis.index(mode)
        instrument.wavelengths[channel] = dblval

        # ...and update wavelength information text in the GUI.
        wavelength_texts = (
            f'\nChannel {channel + 1} wavelength: {wavelength:.8f}'
            for channel, wavelength in sorted(instrument.wavelengths.items())
        )
        instrument.button.config(text=instrument.info + ''.join(wavelength_texts))

# Load wlmData library. If needed, adjust the path by passing it to LoadDLL()!
try:
    dll = wlmData.LoadDLL()
    #dll = wlmData.LoadDLL('/path/to/your/libwlmData.so')
except OSError as err:
    sys.exit(f'{err}\nPlease check if the wlmData DLL is installed correctly!')

# Create GUI
root = tk.Tk()
root.title('Wavelength meter list')
refresh_button = tk.Button(root, text='Refresh', command=refresh)
refresh_button.pack()

# Populate it with wavelength meter list
refresh()

# Initialize wlmData callback function for live update of wavelengths
dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyInstallCallbackEx, callback_ex, 0)

# Run GUI
root.mainloop()

# Cleanup
dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyRemoveCallback, 0, 0)
