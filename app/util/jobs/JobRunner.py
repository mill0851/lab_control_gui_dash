from .Job import Job
from threading import Thread



class JobRunner:
    def __init__(self):
        self.jobs = {}

    def submit(self, func):
        job = Job(func)
        self.jobs[job.id] = job
        Thread(target=job.run, daemon=True).start()
        return job

    def get(self, job_id):
        return self.jobs[job_id]