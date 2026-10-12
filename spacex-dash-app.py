import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

spacex_df = pd.read_csv("spacex_launch_dash.csv")

min_payload = float(spacex_df["Payload Mass (kg)"].min())
max_payload = float(spacex_df["Payload Mass (kg)"].max())

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center"}
        ),

        html.Label("Select a launch site:"),

        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "ALL"}
            ] + [
                {"label": site, "value": site}
                for site in sorted(spacex_df["Launch Site"].unique())
            ],
            value="ALL",
            placeholder="Select a Launch Site here",
            searchable=True,
            clearable=False
        ),

        dcc.Graph(id="success-pie-chart"),

        html.Label("Select payload range (kg):"),

        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            marks={
                value: str(value)
                for value in range(0, 10001, 1000)
            },
            value=[min_payload, max_payload],
            tooltip={"placement": "bottom", "always_visible": True}
        ),

        dcc.Graph(id="success-payload-scatter-chart")
    ],
    style={
        "maxWidth": "1100px",
        "margin": "auto",
        "padding": "25px",
        "fontFamily": "Arial"
    }
)


@app.callback(
    Output("success-pie-chart", "figure"),
    Input("site-dropdown", "value")
)
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        successes = (
            spacex_df.groupby("Launch Site", as_index=False)["class"]
            .sum()
        )

        return px.pie(
            successes,
            values="class",
            names="Launch Site",
            title="Successful Landings by Launch Site"
        )

    filtered_df = spacex_df[
        spacex_df["Launch Site"] == entered_site
    ].copy()

    filtered_df["Outcome"] = filtered_df["class"].map({
        0: "Unsuccessful",
        1: "Success"
    })

    counts = (
        filtered_df.groupby("Outcome")
        .size()
        .reset_index(name="Count")
    )

    return px.pie(
        counts,
        values="Count",
        names="Outcome",
        title=f"Landing Outcomes: {entered_site}",
        color="Outcome",
        color_discrete_map={
            "Success": "green",
            "Unsuccessful": "red"
        }
    )


@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    Input("site-dropdown", "value"),
    Input("payload-slider", "value")
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range

    filtered_df = spacex_df[
        spacex_df["Payload Mass (kg)"].between(low, high)
    ].copy()

    if entered_site != "ALL":
        filtered_df = filtered_df[
            filtered_df["Launch Site"] == entered_site
        ]

    fig = px.scatter(
        filtered_df,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        hover_data=["Launch Site"],
        title=f"Payload and Landing Outcome: {entered_site}",
        labels={"class": "Landing Outcome"}
    )

    fig.update_yaxes(
        tickvals=[0, 1],
        ticktext=["Unsuccessful", "Success"]
    )

    return fig


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
    