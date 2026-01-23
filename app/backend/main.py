from fastapi import FastAPI
from .schemas import ExperimentRequest, Step
from .devices import DeviceManager, LabDevice, DummyScope
from .jobs import JobRunner, Job
from threading import Thread
import time


device_manager = DeviceManager()
device_manager.register(DummyScope("scope1"))
device_manager.register(DummyScope("scope2"))
job_runner = JobRunner()

app = FastAPI()

@app.get("/devices")
def list_devices():
    return device_manager.list_devices()

@app.post("/experiments")
def submit_experiment(exp: ExperimentRequest):
    def job_func():
        results = []
        # Sequential steps
        for step in exp.steps:
            device = device_manager.get(step.device)
            device_methods = device.info()["capabilities"]
            if step.action == "wait":
                time.sleep(step.duration)
                results.append({"waited": step.duration})
            elif step.action in device_methods:
                if not device.acquire():
                    raise RuntimeError(f"Device {step.device} busy")
                try:
                    method = getattr(device, step.action)
                    res = method(*step.args)
                    results.append({"device": step.device, "result": res})
                finally:
                    device.release()

        # Parallel steps
        if exp.parallel_groups:
            for group in exp.parallel_groups:
                threads = []
                group_results = [None]*len(group)

                # Creates a thread to run each 
                def make_thread(i, step):
                    def thread_func():
                        device = device_manager.get(step.device)
                        if not device.acquire():
                            raise RuntimeError(f"Device {step.device} busy")
                        try:
                            group_results[i] = {"device": step.device,
                                                "result": device.measure(step.duration)}
                        finally:
                            device.release()
                    return Thread(target=thread_func)
                
                for i, step in enumerate(group):
                    t = make_thread(i, step)
                    threads.append(t)
                    t.start()
                for t in threads:
                    t.join()
                results.extend(group_results)
        return results
    job = job_runner.submit(job_func)
    return {"job_id": job.id}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = job_runner.get(job_id)
    return {"status": job.status, "result": job.result, "error": job.error}
