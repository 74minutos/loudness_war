import dash
import urllib.request
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

url_data = "https://github.com/74minutos/loudness_war/releases/download/streamlit/joined_data.csv"
data = pd.read_csv(urllib.request.urlopen(url_data), delimiter=";", nrows=100000)
data["time"] = pd.to_datetime(data["time"], unit='m')

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Loudness analysis in over 6.000 songs"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🎧", className="header-emoji"),
                html.H1(
                    children="Loudness Analytics", className="header-title"
                ),
                html.P(
                    children="Analyzing loudness ratio on over 6.000 songs",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Search your Song", className="menu-title"),
                        dcc.Dropdown(
                            id="song_filter",
                            options=[
                                {"label": song , "value": song}
                                for song in np.sort((data.track_name + " - " + data.artist_name).unique())
                            ],
                            value="Stairway to Heaven",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("price-chart", "figure"),
    [
        Input("song_filter", "value"),
    ],
)
def update_charts(track_name):
    mask = (
        (data.track_name + " - " + data.artist_name == track_name)
    )
    filtered_data = data.loc[mask, :]
    loudness_figure = {
        "data": [
            {
                "x": filtered_data["time"],
                "y": filtered_data["loudness"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {
                "text": "Loudness ratio of {}".format((filtered_data.track_name + " - " + filtered_data.artist_name).unique()),
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    return loudness_figure


if __name__ == "__main__":
    app.run_server(debug=True)
