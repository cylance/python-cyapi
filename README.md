# Summary

This Library provides python bindings to interact with the Cylance API. Examples have been created for you in the Examples/ directory, and provide a majority of the common code you'll need to get setup. In order to utilize this Library, you will need an API token from the API Integrations tab inside of the Cylance Console.

# Supported Systems
* Python 2.7 & Python 3 Compatible
* Windows
* Mac

# Installation

```
pip install cyapi
```

# Example

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

creds.json:
```
{
    "tid": "123456-55555-66666-888888888",
    "app_id": "11111111-222222-33333-44444444",
    "app_secret": "555555-666666-222222-444444",
    "region": "NA"
}
```

This file can then be passed in by passing -c path/to/creds.json to any of the examples

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)