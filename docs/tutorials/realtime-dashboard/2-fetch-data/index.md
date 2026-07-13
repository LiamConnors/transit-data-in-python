---
icon: lucide/download
description: Fetch live transit data from the STM API.
---

# Fetch live transit data

In this unit, you'll fetch transit data from the STM API. First, you'll learn what GTFS is.

## What is GTFS?

The General Transit Feed Specification (GTFS) is an open standard for transit data. It means different organizations can publish their transit data in a format that software applications can consume.

There are two specifications:

- **GTFS Schedule** — static data like routes, stops, and timetables
- **GTFS Realtime** — live updates on vehicle positions, trip updates, and service alerts

!!! tip
    For more details, see the [GTFS specification docs](https://gtfs.org/) and the [GTFS Realtime overview](https://gtfs.org/realtime/).

## GTFS Realtime feeds

GTFS Realtime provides several feed types:

- **Vehicle positions** — where vehicles are right now
- **Trip updates** — delays, cancellations, and schedule changes
- **Service alerts** — disruptions and detours

## Get an API key

To access realtime data, you need an STM API key.

Sign up at the [STM Developer Portal](https://portail.developpeurs.stm.info/apihub/) and sign in.

Then:

1. Create a new application following the instructions in the [Wiki guide](https://portail.developpeurs.stm.info/apihub/#/wiki?mode=view&uri=User_guide)
2. Add the **Données Ouverte iBUS - GTFS-Realtime (v2.0)** API to your application
3. Go to **Applications**, select your app, and find **Authentication & Credentials**
4. Copy your API key

!!! warning
    Keep your API key private. Don't commit it to version control.

## Your first request

Open the `transit-dashboard` directory in VS Code or your preferred editor, then let's fetch vehicle positions from the STM API.

### Set your API key

First, set your API key as an environment variable so you don't hardcode it in your script.

=== "macOS / Linux"

    <!-- no-test -->
    ```sh
    export STM_API_KEY="your-api-key-here"
    ```

=== "Windows (PowerShell)"

    <!-- no-test -->
    ```powershell
    $env:STM_API_KEY="your-api-key-here"
    ```

### The code

Create a file called `first_request.py`:

```python
import os
import requests

url = "https://api.stm.info/pub/od/gtfs-rt/ic/v2/vehiclePositions"
headers = {
    "accept": "application/x-protobuf",
    "apiKey": os.environ["STM_API_KEY"],
}

response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.content)} bytes")
```

### Run it

<!-- no-test -->
```sh
python first_request.py
```

You should see something like:

```
Status: 200
Content length: 62720 bytes
```

### The code explained

- We set our API key as an environment variable
- We read it in Python using `os.environ`
- We made a GET request to the vehicle positions endpoint
- We got back binary data — not JSON, but Protocol Buffer format

If you try to print `response.text`, you'll see garbled output. That's because the data is serialized using Protocol Buffers, a binary format. In the next unit, we'll learn how to parse it.
