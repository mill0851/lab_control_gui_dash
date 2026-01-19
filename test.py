import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Test Data
# df = pd.read_csv("tweets.csv")
# df["name"] = pd.Series(df["name"]).str.lower()
# df["date_time"] = pd.to_datetime(df["date_time"], dayfirst=True)
# df = (
#     df.groupby([df["date_time"].dt.date, "name"])[
#         ["number_of_likes", "number_of_shares"]
#     ]
#     .mean()
#     .astype(int)
# )
# df = df.reset_index()


# ---- App Layout ----
stylesheets = ["./assets/main.css"]
app = Dash(__name__, external_stylesheets=stylesheets)

app.layout = html.Div([
    html.Div(
        html.H1(
            "Hello World - Row 1",
            style={"textAlign":"center"}
        ),
        className="row"
    ),
    html.Div(
        html.H1(
            "Hello World - Row 2",
            style={"textAlign":"center"}
        ),
        className="row"
    ),
    html.Div(
        html.H1(
            "Hello World - Row 3",
            style={"textAlign":"center"}
        ),
        className="row"
    )
])

# ---- Run Application ----
if __name__ == "__main__":
    app.run(debug=True)