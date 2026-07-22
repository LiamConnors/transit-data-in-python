---
icon: lucide/download
description: Fetch live transit data from the STM API.
---

# Fetch live transit data

In this section you'll learn what GTFS is and how to make a request to the [Société de transport de Montréal's Realtime API](https://www.stm.info/en/about/developers) using Python.

## What is GTFS?

The General Transit Feed Specification (GTFS) is an open standard for transit data. It means different organizations can publish their transit data in a standard format that software applications can consume.

There are two specifications:

- **GTFS Schedule** — static data like routes, stops, and timetables
- **GTFS Realtime** — live updates on vehicle positions, trip updates, and service alerts

!!! tip
    For more details, see the [GTFS specification docs](https://gtfs.org/) and the [GTFS Realtime overview](https://gtfs.org/realtime/).

### GTFS Realtime feeds

GTFS Realtime provides several feed types:

- **Vehicle positions** — where vehicles are right now
- **Trip updates** — delays, cancellations, and schedule changes
- **Service alerts** — disruptions and detours

## Get an API key

To access realtime data from a transit organisation, you'll generally need an API key. To get a key for STM Realtime data, sign up at the [STM Developer Portal](https://portail.developpeurs.stm.info/apihub/).

Then:

1. Sign in and create a new application following the instructions in the [Wiki guide](https://portail.developpeurs.stm.info/apihub/#/wiki?mode=view&uri=User_guide)
2. Add the **Données Ouverte iBUS - GTFS-Realtime (v2.0)** API to your application
3. Go to **Applications**, select your app, and find **Authentication & Credentials**
4. Copy your API key

## Your first request

Open the `transit-dashboard` directory in VS Code or your preferred editor.

### Set your API key

First, set your API key as an environment variable:

=== "macOS / Linux"

    <!-- no-test -->
    ```sh
    export STM_API_KEY="<your-api-key-here>"
    ```

=== "Windows (PowerShell)"

    <!-- no-test -->
    ```powershell
    $env:STM_API_KEY="<your-api-key-here>"
    ```

### Write the code

Create a file called `first_request.py` and add the following code:

```python linenums="1"
import os
import requests

URL = "https://api.stm.info/pub/od/gtfs-rt/ic/v2/vehiclePositions"
headers = {
    "accept": "application/x-protobuf",
    "apiKey": os.environ["STM_API_KEY"],
}

response = requests.get(URL, headers=headers)
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.content)} bytes")
print(f"First 100 characters: {response.content[:100]}")
```

- Lines 1-2: Import required modules (`os` and `requests`)
- Line 4: Define the API endpoint URL. This comes from the STM developer portal (it is displayed in **APIs** > **Données Ouverte iBUS - GTFS-Realtime (v2.0)** > **Specs** > **Positions**).
- Lines 5-8: Create headers dictionary with accept header and the API key loaded from environment variable
- Line 10: Make a GET request to the endpoint and store the response in the `response` variable
- Lines 11-13: The `response` variable is a `Response` object. Print its status code, content length, and the first 100 characters of the content.

### Run it

In your terminal, run the code with:

<!-- no-test -->
```sh
python first_request.py
```

You'll see output like this:

```
Status: 200
Content length: 58163 bytes
First 100 characters: b'\n\r\n\x032.0\x10\x00\x18\xd2\xa9\xd9\xd2\x06\x12b\n\x0539076"Y\n%\n\t301233716\x12\x0811:14:00\x1a\x0820260714*\x02320\x0...
```

- Status 200 means the request was a success.
- The first 100 characters are Protocol Buffer data, not readable text. That's normal — you need a library to parse it into something human-readable.

Congratulations, you've made your first request to a GTFS Realtime API and received live transit data! Next, you'll learn how to parse the response into readable vehicle positions.

