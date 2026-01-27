from .context import _active_group

class Group:
    def __init__(self, name=None):
        self.name = name
        self.steps = []


    def plan(self, fn):
        # Automatically execute the function upon decoration
        token = _active_group.set(self)
        try:
            fn()  # Execute the plan immediately
        finally:
            _active_group.set(token)
        return fn