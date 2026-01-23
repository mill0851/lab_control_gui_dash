from .Job import Job
from .JobRunner import JobRunner
from time import sleep

if __name__ == "__main__":
    def target_function():
        print("This function does nothing lol")
        sleep(10)

    job_runner = JobRunner()
    job = job_runner.submit(target_function)
    print(job.status)
    print("waiting for completion...")
    sleep(12)
    print(job.status)
