from pyLabLib.pylablib.devices.HighFinesse.wlm import WLM


# Connect to device
print("Locating avilable devices...")
print()
wlm = WLM()
device_info = wlm.get_device_info()
if not wlm.is_opened():
    raise ConnectionError("No Device Found")
print("Device connected:")
print(f"Model: {device_info[0]}")
print(f"Serial number: {device_info[1]}")
print(f"Revision number: {device_info[2]}")
print(f"Compilation number: {device_info[3]}")
print(f"Number of available channels: {wlm.get_channels_number()}")
print()

# Current measurement settings
print("Current system settings:")
print(f"Exposure mode: {wlm.get_exposure_mode()}")
print(f"Exposure (s): {wlm.get_exposure()}")
print(f"Active channel: {wlm.get_active_channel()}")
print(f"Pulse mode: {wlm.get_pulse_mode()}")
print()

# Run quick measurement test
print("Current system readings:")
print(f"Frequency (GHz): {round(wlm.get_frequency() * 1e-9, 6)}")
print(f"Wavelength (nm): {round(wlm.get_wavelength() * 1e9, 2)}")
print()

