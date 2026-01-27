import asyncio
from LabClient import LabClient
from DeviceProxy import DeviceProxy 
from Experiment import Experiment
import numpy as np


async def main():

    # ---- ESTABLISH CONNECTION TO SERVER ----
    client = LabClient("ws://localhost:8000/ws")
    await client.connect()

    # ---- EXPERIMENT ----
    async with Experiment(client) as exp:

        # ---- RESERVE AND INSTANTIATE DEVICES ----
        duration = 3000
        await exp.reserve("DummySpectrometer", duration_s=duration)
        await exp.reserve("DummyStage", duration_s=duration)
        await exp.reserve("DummyVoltage", duration_s=duration)
        spectro = DeviceProxy(client, "DummySpectrometer")
        stage = DeviceProxy(client, "DummyStage")
        voltage_supply = DeviceProxy(client, "DummyVoltage")

        # ---- HELPER FUNCTIONS ----
        async def pl_measurement(voltage_supply, spectrometer, volt_range=(-1.0, 1.0), step=0.25):
            voltages = np.arange(volt_range[0], volt_range[1]+(step/10), step)
            result = []

            for voltage in voltages:
                voltage_supply.set_voltage(voltage)
                data_slice = await spectrometer.capture(exposure=10)
                result.append(data_slice)

            return result

        # ---- EXPERIMENT LOGIC ----
        # Imagine moving across a grid and taking a PL measurement at each spot
        coordinates = [
            (0,0), (1,0), (2,0),
            (0,1), (1,1), (2,1),
            (0,2), (1,2), (2,2)
        ]

        pl_measurements = []

        for coord in coordinates:
            await stage.move(position=coord)
            pl = await pl_measurement(voltage_supply, spectro, volt_range=(-1.5,1.5), step=0.1)
            pl_measurements.append(pl)

    return pl_measurements


# Start Experiment
data = asyncio.run(main())