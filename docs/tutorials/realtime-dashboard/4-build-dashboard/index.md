---
icon: lucide/layout-dashboard
description: Build an interactive dashboard with Dash and Plotly.
---

# Build an interactive dashboard

Now let's display the vehicle positions on an interactive map.

## The code

Create a file called `app.py`:

```python
import os
import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import requests
from google.transit import gtfs_realtime_pb2

def fetch_vehicle_positions():
    url = "https://api.stm.info/pub/od/gtfs-rt/ic/v2/vehiclePositions"
    headers = {
        "accept": "application/x-protobuf",
        "apiKey": os.environ["STM_API_KEY"],
    }
    response = requests.get(url, headers=headers)
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    positions = []
    for entity in feed.entity:
        if entity.HasField("vehicle"):
            vehicle = entity.vehicle
            position = vehicle.position
            label = vehicle.vehicle.id
            if vehicle.HasField("trip"):
                label = vehicle.trip.route_id
            positions.append({
                "label": label,
                "lat": position.latitude,
                "lon": position.longitude,
                "speed": position.speed,
            })
    return positions

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id="map",
        style={"height": "100vh", "width": "100vw"},
        config={"scrollZoom": True},
    ),
    dcc.Interval(id="refresh", interval=10_000, n_intervals=0),
], style={"margin": "0", "padding": "0", "height": "100vh", "overflow": "hidden"})

@app.callback(
    Output("map", "figure"),
    Input("refresh", "n_intervals"),
    prevent_initial_call=False,
)
def update_map(n):
    positions = fetch_vehicle_positions()
    fig = go.Figure(go.Scattermap(
        lat=[p["lat"] for p in positions],
        lon=[p["lon"] for p in positions],
        text=[p["label"] for p in positions],
        hovertext=[f"Route {p['label']} - {p['speed']} km/h" for p in positions],
        mode="markers+text",
        textposition="top center",
        marker=dict(size=12, color="red", allowoverlap=True),
    ))
    fig.update_layout(
        map=dict(
            style="open-street-map",
            center={"lat": 45.5236, "lon": -73.5830},
            zoom=14,
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor="white",
        uirevision="keep-view",
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)
```

## Run it

<!-- no-test -->
```sh
python app.py
```

Open [http://localhost:8050](http://localhost:8050) in your browser. You should see a map of the Plateau area with labeled dots representing buses, each showing its route number.

## What you can do

- **See bus routes** — each dot shows the route number as it moves
- **Auto-refresh** — the map updates every 10 seconds automatically
- **Pan and zoom** — explore the map without losing your view on refresh

!!! note "API rate limits"
    The STM API allows 10 requests/second and 10,000 requests/day per account. The 10-second refresh interval keeps us well within these limits.

## The code explained

- We fetch vehicle positions from the STM API
- We parse the Protocol Buffer response
- We display the positions on a full-screen map centered on the Plateau
- Each bus shows its route number as a label
- The map preserves your zoom and pan position on refresh