1-wire Low-Level Django based REST API
======================================

This project exposes a very simple/low-level REST API leveraging
the Django REST framework on top of the [owfs server](http://owfs.org/)

Devices (sensors, etc.) are automatically discovered and enumerated.
By default, anonymous access to the API can discover all devices, but
only logged in users can write to the devices to modify their state.


Usage
-----

    docker-compose build
    OW_SERVER=<ipaddr> docker-compose up


Then point your browser to http://localhost/devices and you should
see a list of all the 1-wire devices.
