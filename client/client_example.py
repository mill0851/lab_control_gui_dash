from .lab import Lab
from .group import Group

# Example of how to use device proxy class for remote experiment submission


# Instantiate lab object, this is your gateway to controlling the lab devices
lab = Lab("http://lab-server:8000")


# Create device proxies
scope1 = lab.device("dummy_scope1")
scope2 = lab.device("dummy_scope2")


# Create experimental groups. The idea here is that
# you can send multiple measurments to run at the same time
g1 = Group()
g2 = Group()


# Add experimental plan to their respective groups
@g1.plan
def exp1():
    scope1.volt_longterm(
        channel=1,
        duration=15,
        interval=0.025
    )

@g2.plan
def exp2():
    scope2.volt_longterm(
        channel=1,
        duration=15,
        interval=0.025
    )

# Send experiment for submission
job = lab.run(g1, g2)
results = job.wait()