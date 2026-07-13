---
icon: lucide/code
description: Make your first request to the STM API.
---

# Your first request

Open the `transit-dashboard` directory in VS Code or your preferred editor, then let's fetch vehicle positions from the STM API.

## Set your API key

First, set your API key as an environment variable so you don't hardcode it in your script.

=== "macOS / Linux"

    ```sh
    export STM_API_KEY="your-api-key-here"
    ```

=== "Windows (PowerShell)"

    ```powershell
    $env:STM_API_KEY="your-api-key-here"
    ```

## The code

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

## Run it

```sh
python first_request.py
```

You should see:

```
Status: 200
Content length: 12345 bytes
```

## What just happened?

- We set our API key as an environment variable
- We read it in Python using `os.environ`
- We made a GET request to the vehicle positions endpoint
- We got back binary data (Protocol Buffer format)
