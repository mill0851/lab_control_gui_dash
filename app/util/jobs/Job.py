import uuid

class Job:
    def __init__(self, func):
        self.id = str(uuid.uuid4())
        self.func = func
        self.status = "queued"
        self.result = None
        self.error = None

    def run(self):
        try:
            self.status = "running"
            self.result = self.func()
            self.status = "finished"
        except Exception as e:
            self.error = str(e)
            self.status = "failed"