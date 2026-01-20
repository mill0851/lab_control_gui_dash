import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# ---- Style sheets ----
stylesheets = ["../css/main.css"]
app = Dash(__name__, external_stylesheets=stylesheets)

# ---- App Layout ----
app.layout = html.Div([
    
    # ---- Header ----
    html.Div(
        html.H1("PQT Lab Control"),
        className="row"
    ),

    # ---- Wavemeter Measurement Page ----
    html.Div(
        [
            # Two columns:
            # (1)  live feed area
            # (2)  measurement settings area 
            html.Div(
                html.H1("2"), className="three columns"
            ),
            html.Div(
                html.H1("1"), className="two columns"
            )
        ],
        className="row"
    )
])

# ---- Run Application ----
if __name__ == "__main__":
    app.run(debug=True)