import threading
import time
from collections import deque
from dash import Dash, dcc, html, Input, Output, State, no_update
from dash import callback_context as ctx
from dash_extensions import WebSocket
import plotly.graph_objs as go
from app.util.pyLabLib.pylablib.devices.HighFinesse.wlm import WLM
from app.util.pyLabLib.pylablib.core.devio.interface import DeviceManager


# ---- Config ----
wlm = WLM()
devices = {
    "wlm": wlm
}
device_manager = DeviceManager(devices)


# ---- Application ----
stylesheets = ["../css/main.css"]
app = Dash(__name__, external_stylesheets=stylesheets)

app.layout = html.Div([
    html.H3("Frequency (THz):"),
    html.Button("Update", id="wlm-get-freq", n_clicks=0),
    dcc.Store(id="freq-store"),
    dcc.Interval(id="poll", interval=500), # poll every 0.5s
    html.Div(id="freq")
])


# ---- Callback Functions ----
job_triggers = {
    "wlm-get-freq": {
        "device": "wlm",
        "method": "get_frequency",
        "args": [None, False, True, 5.]
    }
}

@app.callback(
    Output("freq-store", "data"),
    Output("freq", "children"),
    Input("wlm-get-freq", "n_clicks"),
    Input("poll", "n_intervals"),
    State("freq-store", "data"),
    prevent_initial_call=True
)
def freq_state_machine(n_clicks, _intervals, store):
    trigger = ctx.triggered_id

    # ---- Button Click ----
    if trigger == "wlm-get-freq":
        job = job_triggers[trigger]
        response = device_manager.submit_job(job)

        if response["status"] in ["error", "busy", "pending"]:
            return response, response["message"]
        else:
            return response, "error submitting job"

    # ---- Polling ----
    if not store or store["status"] != "pending":
        return no_update, no_update

    job_id = store["job_id"]
    future = device_manager._futures.get(job_id)

    if not future:
        return no_update, no_update

    if future.done():
        result = future.result()
        del device_manager._futures[job_id]

        return (
            {
                "status": "finished",
                "data": result,
                "job_id": job_id,
                "message": f"Job {job_id} complete"
            },
            f"Frequency (THz): {result}"
        )

    return no_update, no_update

# ---- Run Application ----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
    # app.run(debug=True)