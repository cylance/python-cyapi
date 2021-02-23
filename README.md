# Summary

This Library provides python bindings to interact with the Cylance API. Examples have been created for you in the Examples/ directory, and provide a majority of the common code you'll need to get setup. In order to utilize this Library, you will need an API token from the API Integrations tab inside of the Cylance Console.

# Supported Systems
* Python 2.7 & Python 3 Compatible
* Windows
* Mac
* Linux

# Installation

```
pip install cyapi
```

# Example

Please note there are a number of example scripts in the examples directory. These are valuable for initial authentication as well as some basic interactions with the library. The example scripts include:
Single Tenant
> simple_setup.py
> find_stale_devices.py
> safelist_trusted_local.py
> time_getting_all_detection_detail.py

Multi-Tenant Console (MTC)
> simple_MTC_setup.py
> MTC_tenants_loop.py

This example will create a connection to the API and return all devices that have registered.

```
from cyapi.cyapi import CyAPI
from pprint import pprint
API = CyAPI(tid=your_id, aid=your_aid, ase=your_ase)
API.create_conn()
devices = API.get_devices()
print("Successful: {}".format(devices.is_success))
pprint(devices.data[0]) # Print info about a single device.
```

If you have lots of devices/threats/zones/etc, and you'd like to see a progress bar, pass the `disable_progress` parameter:

```
devices = API.get_devices(disable_progress=False)
pprint(devices.data[0])
```

Additionally you can copy examples/simple_setup.py to your_new_file.py and begin hacking away from there.

# Creds File

You can create a file that will store your api credentials instead of passing them in via the command line. The creds file should look like the following:

For a standard tenant:
creds.json:
```
{
    "tid": "123456-55555-66666-888888888",
    "app_id": "11111111-222222-33333-44444444",
    "app_secret": "555555-666666-222222-444444",
    "region": "NA"
}
```

For a Multi-Tenant Console (MTC)
```
{
    "tid": "Not Used for MTC Auth",
    "app_id": "11111111-222222-33333-44444444",
    "app_secret": "555555-666666-222222-444444",
    "region": "NA",
    "mtc": "True"
}
```
The creds json file can then be passed in by passing -c path/to/creds.json to any of the examples

# API End Point Documentation

Tenant User API Guide - https://docs.blackberry.com/content/dam/docs-blackberry-com/release-pdfs/en/cylance-products/api-and-developer-guides/Cylance%20User%20API%20Guide%20v2.0%20rev24.pdf
Tenant User API Release Notes - https://docs.blackberry.com/en/unified-endpoint-security/cylance--products/cylance-api-release-notes/BlackBerry-Cylance-API-release-notes
Multi-Tenant API - https://dev-admin.cylance.com/documentation/api.html

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
