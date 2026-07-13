---
icon: lucide/terminal
description: Parse GTFS Realtime data from the STM API.
---

# Parse real-time vehicle positions

In the previous unit, we fetched data from the STM API and got back binary data. Now let's parse it into something we can use.

## The code

Create a file called `parse_positions.py` and add the following code:

```python
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

## The code explained

- We import `gtfs_realtime_pb2` from the installed package
- We make a GET request to the vehicle positions endpoint
- We create a `FeedMessage` — the root type in the GTFS Realtime schema
- We call `ParseFromString()` to deserialize the binary data
- We loop through the entities and extract vehicle positions

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

## Summary

You fetched realtime bus location data from the STM API and parsed it in Python. The data includes the latitude, longitude, and speed of each bus currently in transit.
