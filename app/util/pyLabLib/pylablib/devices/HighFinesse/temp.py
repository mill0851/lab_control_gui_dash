def get_device_info(self):
    """
    Get the wavemeter info.

    Return tuple ``(model, serial_number, revision_number, compilation_number)``.
    """
    return TDeviceInfo(*[self.lib.GetWLMVersion(i) for i in range(4)])





