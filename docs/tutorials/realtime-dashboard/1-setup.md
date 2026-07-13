---
icon: lucide/folder
description: Create a project directory and install the packages you'll need.
---

# Set up your development environment

In this unit, you'll create the directory for your project and set up a Python environment.

!!! note
    We use Python 3.14 in this tutorial, but any recent Python version (3.10+) will work.

## Create a project directory

In your terminal, go to where you want to build your project, and then create a new directory:

```sh
mkdir transit-dashboard
cd transit-dashboard
```

You should now be inside the `transit-dashboard` directory.

## Set up the Python environment

Next, create and activate a Python virtual environment using [venv](https://docs.python.org/3/library/venv.html). This keeps your project's dependencies isolated from other Python projects.

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
- `gtfs-realtime-bindings` — to parse GTFS Realtime data
- `dash` — a web framework for building interactive dashboards

To install these packages, run:

```sh
pip install requests gtfs-realtime-bindings dash
```

You should see a success message for each package installed.
