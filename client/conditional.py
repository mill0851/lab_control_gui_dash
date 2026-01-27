from .context import _active_group



class If:
    def __init__(self, condition):
        self.condition = condition
        self.then_steps = []
        self.else_steps = []

    def __enter__(self):
        group = _active_group.get()
        group.add(self)
        self._token = _active_group.set(self)
        return self

    def __exit__(self, exc_type, exc, tb):
        _active_group.reset(self._token)

    def add(self, step):
        self.then_steps.append(step)


class Else:
    def __enter__(self):
        parent = _active_group.get()
        parent._token = _active_group.set(parent)
        return parent

    def __exit__(self, exc_type, exc, tb):
        pass