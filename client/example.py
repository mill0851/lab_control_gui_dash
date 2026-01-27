import asyncio
from LabClient import LabClient       # your client class
from DeviceProxy import DeviceProxy   # proxy class
from Experiment import Experiment      # async context manager


async def main():

    # Establish connection to lab computer
    client = LabClient("ws://localhost:8000/ws")
    await client.connect()

    # This is where your experimental logic goes
    async with Experiment(client) as exp:

        # Reserve which devices you will use and how long (device_name, durations_s=duration)
        await exp.reserve("cam1", duration_s=300)
        await exp.reserve("cam2", duration_s=300)

        # Instantiate the devices you want (LabClient, device_name)
        cam1 = DeviceProxy(client, "cam1")
        cam2 = DeviceProxy(client, "cam2")

        # Experimental logic
        img1 = await cam1.capture()
        img2 = await cam2.capture()

        # Display results
        print(img1)
        print(img2)


# Start Experiment
asyncio.run(main())