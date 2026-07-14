---
icon: lucide/folder
description: Create a project directory and install the packages you'll need.
---

# Set up your development environment

In this unit, you'll create the directory for your project and set up a Python environment.

!!! note
    This tutorial uses Python 3.14, but any recent Python version (3.10+) will work.

## Create a project directory

In your terminal, go to where you want to build your project, then create a new directory, and `cd` into that directory:

```sh
mkdir transit-dashboard
cd transit-dashboard
```

## Set up the Python environment

Next, create and activate a Python virtual environment using [venv](https://docs.python.org/3/library/venv.html). Virtual environments keep your project's dependencies isolated from other Python projects on your system.

=== "macOS / Linux"

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

=== "Windows (PowerShell)"

    ```powershell
    python3 -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

!!! tip
    See [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments) for a good intro to working with Python virtual environments in VS Code.

## Install the packages

Now that you have the environment set up and activated, install the following packages:

- `requests` — to fetch data from the API
- `protobuf` — to deserialize the transit data
- `dash` — to build the interactive dashboard

To install these packages, run:

```sh
pip install requests protobuf dash
```

You should see a success message for each package installed.

## Validate the environment

Finally, run `pip list` and you should see a list of packages like the following that includes `requests`, `gtfs-realtime-bindings`.

```sh
Package                Version
---------------------- ---------
annotated-types        0.7.0
blinker                1.9.0
certifi                2026.6.17
charset-normalizer     3.4.9
click                  8.4.2
dash                   4.4.0
Flask                  3.1.3
gtfs-realtime-bindings 2.1.0
...
```
