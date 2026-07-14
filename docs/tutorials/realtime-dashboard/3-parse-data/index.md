---
icon: lucide/terminal
description: Parse GTFS Realtime data from the STM API.
---

# Parse real-time vehicle positions

In the previous section, we made a request to the STM API for Realtime transit data. Now let's parse it into something we can use.

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
        print(f"Vehicle {vehicle.vehicle.id}: "
              f"lat={position.latitude}, "
              f"lon={position.longitude}, "
              f"speed={position.speed}")
```

- Lines 1-3: Import required modules (`os`, `requests`, and `gtfs_realtime_pb2`)
- Line 5: Define the API endpoint URL. This comes from the STM developer portal. It is displayed in **APIs** > **Données Ouverte iBUS - GTFS-Realtime (v2.0)** > **Specs** > **Positions**.
- Lines 6-9: Create headers dictionary with accept header and API key from environment variable. `os.environ` loads the API key from the environment variable we set in the previous section. 
- Line 11: Make GET request to the endpoint using `requests`
- Lines 13-14: Create a `FeedMessage` and parse the binary response data
- Lines 16-24: Loop through entities and extract vehicle positions (latitude, longitude, speed)

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

