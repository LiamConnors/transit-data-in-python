---
icon: lucide/play-circle
---

# Getting Realtime Transit Data from the STM API using Python

I recently used one of the Realtime data APIs provided by [Société de transport de Montréal (STM)](https://www.stm.info/) to get data about bus locations using Python. This tutorial will help you understand how transit data is structured and how to interact with a transit data API in Python.

!!! note "Prerequisites"
    - [Python](https://www.python.org/downloads/). Here, we use Python 3.14, but you can use any recent Python version (3.10+).
    - Basic command line knowledge
    - [VS Code](https://code.visualstudio.com/) or another editor of your choice

## Setting up the project

Before we can start working with the STM API, we need to set up a project directory and install some packages. To set up the project:

1.  Create a directory to store all the data and code for the project — for example, `transit_data_project`.
2.  Create and activate a virtual environment using [venv](https://docs.python.org/3/library/venv.html). See [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments) for a good intro to working with Python virtual environments in VS Code.
3.  In the virtual environment, install the packages we'll use:

```sh
pip install requests protobuf
```

**Note on what we are installing**

-   `requests` to fetch the data.
-   `protobuf` to deserialize the data. More on Protocol Buffers later.

## Creating an account and an API key

To access realtime data, you'll need an STM API key. To get an API key:

1. Sign up to the [STM Developer Portal](https://portail.developpeurs.stm.info/apihub/) and sign in.

2.  Once you have access to the portal, create an application following the instructions for **How to create an application** available in the [Wiki menu](https://portail.developpeurs.stm.info/apihub/#/wiki?mode=view&uri=User_guide). When completing step 4 of the Wiki guide, ensure you add the **Données Ouverte iBUS - GTFS-Realtime (v2.0)** API.

## What is GTFS?

In the previous step, we added the **Données Ouverte iBUS - GTFS-Realtime (v2.0)** API to our STM application. But what is GTFS?

The General Transit Feed Specification (GTFS) is an open standard for transit data that means it can be used by different organisations to publish their transit data and that data can then easily be consumed by software applications.

There is a static data specification known as **GTFS Schedule** and a data specification for providing realtime updates, called **GTFS Realtime**, which is what we are exploring here.

!!! tip
    For more details on GTFS, see the [specification docs](https://gtfs.org/). There's also a good overview of GTFS Realtime [on this Google Developers page](https://developers.google.com/transit/gtfs-realtime/).

### GTFS Realtime

There are a few different aspects to the GTFS Realtime standard: It provides a specification to deliver info on trip updates, service alerts, vehicle positions, and trip modifications.

As of June 2024, it looks like the STM API provides feeds for trip updates and vehicle positions.

!!! tip
    See [Overview of GTFS Realtime feeds](https://gtfs.org/realtime/) for more reading on this.


## Retrieving the API key

To retrieve the API key:

1.  Log in to the portal (if you aren't already) and find the application you created in the **Applications** menu.
2.  Select the application and scroll to **Authentication & Credentials**.
3.  Select the API key name and copy the **API Key**.

## Data from the API

If you've retrieved data from APIs before, you may have seen they often return data in JSON format. You might do something like this to get the data and access the JSON in Python.

```python
import requests
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data = response.json()
```

This snippet uses the [requests library](https://docs.python-requests.org/en/latest/index.html) to make the request, and also to decode the JSON.

The Realtime Data API doesn't return content as JSON, however. It uses Protocol Buffers.

### Protocol Buffers

Protocol Buffers are a way to serialize data. With Protocol Buffers, a schema for the data is defined using a `.proto` file. So, there is a GTFS `.proto` file for Realtime data that describes the structure of that data. You can see that file at [https://gtfs.org/realtime/proto/](https://gtfs.org/realtime/proto/)

Protocol Buffers are language-neutral, and with a `.proto` file, we can compile it for use in different languages, allowing us to read/write data based on the specified format. When we compile the file for Python, we'll get a `.py` file that we can use.

!!! note
    Here, I go through the steps of compiling the .proto file, because I wanted to learn more about Protocol Buffers. However, there are [Python GTFS-realtime Language Bindings](https://gtfs.org/realtime/language-bindings/python/) available on the General Transit Feed Specification website, which mean you can avoid this step. You'll also find a code example there if you want to adapt the code later on this page to use the Python package it provides.

**Compiling the proto file**

**1. Download the compiler.** To compile the .proto file, you need the Protocol Buffers compiler. The latest version at time of writing is available [on the Protocol Buffers releases tab here in GitHub](https://github.com/protocolbuffers/protobuf/releases/tag/v27.1).

**2. Save the .proto file to your project directory** Save the file at [https://gtfs.org/realtime/proto/](https://gtfs.org/realtime/proto/) to your project directory.

**3. `cd` into your project directory in the terminal.**

**4. Run the compiler on the `.proto` file** 
```bash 
protoc --python_out=. gtfs-realtime.proto
```

This will create a `.py` file called `gtfs_realtime_pb2`

See the [Python Generated Code Guide](https://protobuf.dev/reference/python/python-generated/) for a good intro to Protocol Buffers in Python.

### Getting the endpoint

We will also need to know where the data is available to use it in our Python code. This is the API endpoint. To retrieve it:

1.  Go to the **APIs** menu.
2.  Select **Données Ouverte iBUS - GTFS-Realtime (v2.0)**.
3.  Go to the **Specs** tab.
4.  Select **Authorize** and input your API key.
5.  Under **Positions**, select **Try it out**.
6.  Copy the **Request URL**.

## Python code

Open your project directory in your favourite code editor. I use VS Code, which makes it easy to work with Jupyter Notebooks.

Right now in our project directory, we have the `.proto` file, and the Python output from compiling it, in a file called `gtfs_realtime_pb2.py.` Next, we'll want a file to write our code in. In this code, we'll make the request to the STM API and process the response.

In the project directory, create a file called `realtime_data.ipynb` and add the following code. We'll walk through it line by line.

```python
import requests
import gtfs_realtime_pb2

url = "https://api.stm.info/pub/od/gtfs-rt/ic/v2/vehiclePositions"
headers = {
    "accept": "application/x-protobuf",
    "apiKey": "<your-api-key>",  # replace this with your API key
}

response = requests.get(url, headers=headers)

transit_data = response.content

message = gtfs_realtime_pb2.FeedMessage()

message.ParseFromString(transit_data)

message
```

**The code explained**

-   First we import `requests`. This is a Python package for making http requests
-   Then, we import the Python module `gtfs_realtime_pb2`, which is what was generated when we compiled the `.proto` file.
-   Next, we specify the endpoint URL that we want to get the data from. See the **Getting the Endpoint** section from earlier for details on finding this in the STM portal.
-   We declare a `dict` of `headers` to pass with the request to the endpoint, specifying what type of data we accept as a response, and the API key from the STM portal.
-   With `response = requests.get(url, headers=headers)` we make the request to the endpoint.
-   We access the response's content with `response.content` and save it to a variable called transit\_data.
-   With `message = gtfs_realtime_pb2.FeedMessage()` we create an instance of `FeedMessage`, which is the root type in the Realtime schema.
-   That `FeedMessage` object has a `ParseFromString` method that we pass the `transit_data` we received from the API to.
-   Finally, by specifying `message` as the last line of the cell, we can see the output in the notebook.

## Useful resources

-   [Protocol Buffers documentation](https://protobuf.dev/)
-   [General Transit Feed Specification (GTFS) website](https://gtfs.org/)
