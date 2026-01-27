import requests
import time
from .device_proxy import DeviceProxy
import sys
import json

class JobHandle:
    """
    After submitting an experiment this class will poll results until
    the server changes the job status
    """
    def __init__(self, base_url, job_id):
        self.base_url = base_url
        self.job_id = job_id

    def wait(self, poll_interval=0.2):
        while True:
            r = requests.get(
                f"{self.base_url}/jobs/{self.job_id}"
            ).json()

            if r["status"] == "finished":
                return r["result"]

            if r["status"] == "failed":
                raise RuntimeError(r["error"])

            time.sleep(poll_interval)


class Lab:
    """
    This class allows the user to interact with the lab server
    by storing the API endpoints needed to request the execution of
    experiments and use of devices
    """
    def __init__(self, url: str):
        """
        creates the Lab object and stores the target url 

        Args:
            url (str): This is the base url of the target server
        """
        self.url = url

    def device(self, name: str):
        """
        creates a device proxy for the target lab device. This allows
        for the generation of server readable instructions for the 
        execution of hardware API code

        Args:
            name (str): the name of the target device as known
            to the server (see server)

        Returns:
            DeviceProxy: a proxy of a lab device that allows
            users to generate experimental steps
        """
        return DeviceProxy(name)

    def run(self, *groups):
        """
        generates a json payload then sends a post request to the
        lab server. The server will respond with the result of the
        request

        Returns:
            job_id: key used to check job status
        """
        payload = {
            "groups": [g.steps for g in groups]
        }

        print("Experiment (groups run in parallel): ")
        print()
        print(json.dumps(payload, indent=2))
        print()
        validation = input("Would you like to submit this experiment? (y/n): ")
        print()

        if validation == "y":
            print("Expriment submitted")
            print()
            r = requests.post(f"{self.url}/run", json=payload)
            return JobHandle(self.url, r.json()["job_id"])
        else:
            print("Ending experiment request")
            print()
            return None