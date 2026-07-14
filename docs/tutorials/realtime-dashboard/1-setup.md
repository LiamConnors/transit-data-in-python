---
icon: lucide/folder
description: Create a project directory and install the packages you'll need.
---

# Set up your development environment

In this section, you'll create the directory for your project and set up a Python environment.

!!! note
    We use Python 3.14 in this tutorial, but any recent Python version (3.10+) will work.

## Create a project directory

In your terminal, go to where you want to build your project, create a new directory, and `cd` into that directory:

```sh
mkdir transit-dashboard
cd transit-dashboard
```

## Set up the Python environment

Now that you are in the `transit-dashboard` directory, create and activate a Python virtual environment using [venv](https://docs.python.org/3/library/venv.html). Using a virtual environment keeps your project's dependencies isolated from other Python projects on your machine.

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

## Install the required packages

Next, install the following packages in the virtual environment:

- `requests` — to fetch data from the API
- `gtfs-realtime-bindings` — to parse GTFS Realtime data
- `dash` — a web framework for building interactive dashboards

To install these packages, run:

```sh
pip install requests gtfs-realtime-bindings dash
```

You should see a success message for each package installed.

## Validate the environment

Finally, run `pip list` and you should see a list of packages that includes `requests`, `gtfs-realtime-bindings`. You'll also see other packages listed, as each of the packages the project requires also depends on other packages.