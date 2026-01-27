from fastapi import FastAPI, HTTPException
from .schemas import ExperimentRequest, Step
from .devices import DeviceManager, LabDevice, DummyScope
from .jobs import JobRunner, Job
from threading import Thread, Barrier
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
def submit_experiment(exp: ExperimentRequest) -> list:
    """
    The architecture here is for you to submit an "ExperimentRequest". The experiment request is given to a "Job"
    that takes a custom handling function as an argument. The custom handling function should handle errors with
    HTTPException with the proper status_code. Once the job is created the "JobRunner" executes the measurement process
    on the host computer. This JobRunner interacts with the "DeviceManager" to gain device access and permissions. Once
    access is acquired the code executes and data is passed upstream.

    :param exp: ExperimentRequest Object - see schemas
    :return: Returns a list of experimental results based on the "parallel_type" submitted
    If "Sequential" each list of Step objects is run sequentially producing a single array.
    If "Simultaneous" each list of Step objects is run simultaneously using threads. This returns
    a list of lists. the inner lists contain the results for each step. The return is indexed the
    same as the input.
    """

    def job_func():

        def run_step(step: Step, results: list = []):
            try:
                device = device_manager.get(step)
            except KeyError as e:
                 raise HTTPException(status_code=404, detail="Requested device doesnt exist")
            device_methods = device.info()["capabilities"]

            if step.action == "wait":
                time.sleep(step.duration)
                results.append({"waited": step.duration})

            elif step.action in device_methods:
                if not device.acquire():
                    raise HTTPException(status_code=409, detail=f"Device {step.device} busy")
                try:
                    method = getattr(device, step.action)
                    res = method(*step.args)
                    results.append({"device": step.device, "result": res})
                except Exception as e:
                    raise HTTPException(status_code=400, detail=str(e))
                finally:
                    device.release()

            else:
                raise HTTPException(status_code=400, detail="Specified methods unavailable - see device class")              

        if exp.parallel_groups:

            #  CHECK FOR INVALID TYPE
            if exp.parallel_type not in ("sequential", "simultaneous"):
                raise HTTPException(
                    status_code=400,
                    detail="Parallel type must be sequential or simultaneous"
                )
            
            all_results = []

            #  SEQUENTIAL GROUPS (ONE AFTER ANOTHER)
            if exp.parallel_type == "sequential":
                for group in exp.parellel_groups:
                    group_results = []
                    for step in group:
                        run_step(step, group_results)
                    all_results.append(group_results)
                        
            #  SIMULTANEOUS GROUPS (ALL RUN IN PARALLEL)
            else:
                threads = []
                group_results = [None]*len(exp.parallel_groups)
                start_barrier = Barrier(len(exp.parallel_groups))
                
                def run_group(idx: int, steps: list):
                    start_barrier.wait()
                    local_results = []
                    for step in steps:
                        run_step(step, local_results)
                    group_results[idx] = local_results

                for i, group in enumerate(exp.parallel_groups):
                    t = Thread(
                        target=run_group,
                        args=(i, group),
                        daemon=True
                    )
                    threads.append(t)
                    t.start()

                for t in threads:
                    t.join()

                all_results = group_results

        return  all_results

    job = job_runner.submit(job_func)
    return {"job_id": job.id}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = job_runner.get(job_id)
    return {"status": job.status, "result": job.result, "error": job.error}
