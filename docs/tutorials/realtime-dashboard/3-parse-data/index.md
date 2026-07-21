---
icon: lucide/terminal
description: Parse GTFS Realtime data from the STM API.
---

# Parse real-time vehicle positions

In the previous section, you made a request to the STM API for Realtime transit data. Now let's parse it into something you can use.

## The code

Create a file called `parse_positions.py` and add the following code:

```python linenums="1"
import os
import requests
from google.transit import gtfs_realtime_pb2

url = "https://api.stm.info/pub/od/gtfs-rt/ic/v2/vehiclePositions"
headers = {
    "accept": "application/x-protobuf",
    "apiKey": os.environ["STM_API_KEY"],
}

response = requests.get(url, headers=headers)

feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)

for entity in feed.entity:
    if entity.HasField("vehicle"):
        vehicle = entity.vehicle
        position = vehicle.position
        print(
            f"Vehicle {vehicle.vehicle.id}: "
            f"lat={position.latitude}, "
            f"lon={position.longitude}, "
            f"speed={position.speed}"
        )
```

- Lines 1-3: Import required modules (`os`, `requests`, and `gtfs_realtime_pb2`)
- Line 5: Define the API endpoint URL. This comes from the STM developer portal. It is displayed in **APIs** > **Données Ouverte iBUS - GTFS-Realtime (v2.0)** > **Specs** > **Positions**.
- Lines 6-9: Create headers dictionary with accept header and API key from environment variable. `os.environ` loads the API key from the environment variable you set in the previous section.
- Line 11: Make GET request to the endpoint using `requests`
- Lines 13-14: Create an empty `FeedMessage` and parse the binary response into it. A GTFS Realtime feed is a `FeedMessage` containing a list of `entity` records. Each entity can represent different things — a vehicle position, a trip update, or a service alert.
- Line 17: Before accessing the `vehicle` field on an entity, the code checks `HasField("vehicle")` to make sure this entity actually carries a vehicle position. Not all entities do — some might be alerts or updates — so this guard prevents runtime errors.
- Lines 18-25: Each vehicle entity carries a `VehiclePosition` with a `position` (lat/lon/speed) and a `vehicle` descriptor. In `vehicle.vehicle.id`: the variable `vehicle` is the `VehiclePosition`, `.vehicle` is the `VehicleDescriptor`, and `.id` is the bus number.

## Run it

<!-- no-test -->
```sh
python parse_positions.py
```

You should see output like:

```
Vehicle 80012: lat=45.510, lon=-73.564, speed=14.0
Vehicle 80014: lat=45.522, lon=-73.578, speed=0.0
...
```

Congratulations, you've parsed your first GTFS Realtime feed! Next, you'll build an interactive dashboard to visualize these vehicle positions on a map.

