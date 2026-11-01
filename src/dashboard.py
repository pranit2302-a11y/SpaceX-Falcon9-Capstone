from pathlib import Path
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

DATA = Path("data/dataset_part_1.csv")
if not DATA.exists():
    raise SystemExit("Missing data/dataset_part_1.csv. Run src/download_data.py first.")

df = pd.read_csv(DATA)
df["class"] = pd.to_numeric(df["class"], errors="coerce")
df["payload_mass"] = pd.to_numeric(df["payload_mass"], errors="coerce")
df = df.dropna(subset=["class"]).copy()
df["class"] = df["class"].astype(int)
df["class_label"] = df["class"].map({0: "Unsuccessful landing", 1: "Successful landing"})
df["launch_site"] = df["launch_site"].fillna("Unknown")
df["orbit"] = df["orbit"].fillna("Unknown")

app = Dash(__name__)
app.title = "SpaceX Falcon 9 Landing Dashboard"
app.layout = html.Div([
    html.H1("SpaceX Falcon 9 — First-stage Landing Dashboard"),
    html.P("Interactive exploration of historical first-stage landing outcomes."),
    html.Label("Launch site"),
    dcc.Dropdown(options=[{"label": "All sites", "value": "All"}] +
                 [{"label": x, "value": x} for x in sorted(df["launch_site"].unique())],
                 value="All", clearable=False, id="site-filter"),
    html.Label("Orbit"),
    dcc.Dropdown(options=[{"label": "All orbits", "value": "All"}] +
                 [{"label": x, "value": x} for x in sorted(df["orbit"].unique())],
                 value="All", clearable=False, id="orbit-filter"),
    dcc.Graph(id="successful-site-pie"),
    dcc.Graph(id="orbit-success-bar"),
    dcc.Graph(id="payload-outcome-scatter"),
], style={"maxWidth": "1180px", "margin": "28px auto", "fontFamily": "Arial"})

@app.callback(
    Output("successful-site-pie", "figure"),
    Output("orbit-success-bar", "figure"),
    Output("payload-outcome-scatter", "figure"),
    Input("site-filter", "value"),
    Input("orbit-filter", "value"),
)
def update_dashboard(site, orbit):
    d = df.copy()
    if site != "All":
        d = d[d["launch_site"] == site]
    if orbit != "All":
        d = d[d["orbit"] == orbit]
    site_summary = d.groupby("launch_site", as_index=False).agg(
        successful_launches=("class", "sum"), total_launches=("class", "size"))
    pie = px.pie(site_summary, names="launch_site", values="successful_launches",
                 title="Successful Launches by Site", hover_data=["total_launches"], hole=0.25)
    orbit_summary = d.groupby("orbit", as_index=False).agg(
        success_rate=("class", "mean"), launches=("class", "size"))
    orbit_summary["success_rate_pct"] = 100 * orbit_summary["success_rate"]
    bar = px.bar(orbit_summary, x="orbit", y="success_rate_pct", hover_data=["launches"],
                 range_y=[0, 100], title="Landing Success Rate by Orbit",
                 labels={"orbit": "Orbit", "success_rate_pct": "Landing success rate (%)"},
                 text_auto=".1f")
    scatter_data = d.dropna(subset=["payload_mass"]).copy()
    scatter = px.scatter(scatter_data, x="payload_mass", y="class_label", color="class_label",
        hover_data=[c for c in ["flight_number", "launch_site", "orbit", "booster_version"] if c in scatter_data],
        title="Payload Mass vs. Landing Outcome",
        labels={"payload_mass": "Payload mass (kg)", "class_label": "Landing outcome"})
    return pie, bar, scatter

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=8050)
