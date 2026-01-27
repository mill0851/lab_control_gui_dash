from .context import _active_group

class DeviceProxy:
    def __init__(self, device_name: str):
        self.device_name = device_name

    def __getattr__(self, method_name):
        def recorder(**kwargs):

            group = _active_group.get(None)
            if group is None:
                raise RuntimeError(
                    "Device method called outside of a Group plan"
                )

            group.steps.append({
                "type": "command",
                "device": self.device_name,
                "method": method_name,
                "params": kwargs
            })
            
        return recorder