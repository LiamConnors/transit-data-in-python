---
icon: lucide/book-open
description: Understand GTFS and GTFS Realtime data.
---

# Understand GTFS

In this unit, you'll fetch transit data from the STM API, but before doing that you'll need to understand what GTFS is.

## What is GTFS?

The General Transit Feed Specification (GTFS) is an open standard for transit data. It means different organisations can publish their transit data in a format that software applications can easily consume.

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
