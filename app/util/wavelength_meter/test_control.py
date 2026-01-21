from app.util.pyLabLib.pylablib.devices.HighFinesse import wlm
from time import sleep

if __name__=="__main__":

    wlm = wlm.WLM(autostart=True)
    sleep(60)
    wlm.close()
