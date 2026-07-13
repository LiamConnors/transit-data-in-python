---
icon: lucide/folder
description: Create a project directory and install the packages you'll need.
---

# Set up your development environment

In this unit, you'll create the directory structure for your project and set up a Python environment.

!!! note
    We use Python 3.14 in this tutorial, but any recent Python version (3.10+) will work.

## Create a project directory

In your terminal, go to where you want to save your project, and then create a new directory:

```sh
mkdir transit-dashboard
cd transit-dashboard
```

## Set up the Python environment

Next, create and activate a Python virtual environment using [venv](https://docs.python.org/3/library/venv.html). Virtual environments keep your project's dependencies isolated from other Python projects on your system.

=== "macOS / Linux"

    ```sh
    python3 -m venv venv
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

Now that you have the environment set up and activated, install the packages you'll need. You'll need:

- `requests` — to fetch data from the API
- `protobuf` — to deserialize the transit data
- `dash` — to build the interactive dashboard

To install these packages, run:

```sh
pip install requests protobuf dash
```


## Checklist

- [ ] I have created a project directory
- [ ] I have activated a virtual environment
- [ ] I have installed `requests`, `protobuf`, and `dash`
