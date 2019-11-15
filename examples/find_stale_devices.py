# Simple example to read creds file, connect to API, and print detections.
from __future__ import print_function

import argparse
import json
from datetime import datetime, timedelta
from pprint import pprint

import pytz

from cyapi.cyapi import CyAPI, debug_level

__VERSION__ = '1.0'

##################################################################################
# Arguments
#
##################################################################################
def ParseArgs():

    regions = []
    regions_help =  "Region the tenant is located: "
    for (k, v) in CyAPI.regions.items():
        regions.append(k)
        regions_help += " {} - {} ".format(k,v['fullname'])

    parser = argparse.ArgumentParser(description='Find all devices that have been offline for XX days (default: 30)', add_help=True)
    parser.add_argument('-v', '--verbose', action="count", default=0, dest="debug_level",
                        help='Show process location, comments and api responses')
    # Cylance SE Tenant
    parser.add_argument('-tid', '--tid_val', help='Tenant Unique Identifier')
    parser.add_argument('-aid', '--app_id', help='Application Unique Identifier')
    parser.add_argument('-ase', '--app_secret', help='Application Secret')
    parser.add_argument('-c', '--creds_file', dest='creds', help='Path to JSON File with API info provided')
    parser.add_argument('-r', '--region', dest='region', help=regions_help, choices=regions, default='NA')
    parser.add_argument('-d', '--days', dest='days', default=30, help='Number of days to check')

    return parser

##################################################################################
# Tenant Integration
# Modify the keys to align with your tenant API
##################################################################################

commandline = ParseArgs()
args = commandline.parse_args()

if args.debug_level:
    debug_level = args.debug_level

if args.creds:
    with open(args.creds, 'rb') as f:
        creds = json.loads(f.read())

    if not creds.get('region'):
        creds['region'] = args.region

    API = CyAPI(**creds)

elif args.tid_val and args.app_id and args.app_secret:
    tid_val = args.tid_val
    app_id = args.app_id
    app_secret = args.app_secret
    API = CyAPI(tid_val,app_id,app_secret,args.region)

else:
    print("[-] Must provide valid token information")
    exit(-1)

API.create_conn()
devices = API.get_devices()
detailed_devices = []

before = datetime.utcnow() - timedelta(days=int(args.days))
device_ids = [d['id'] for d in devices.data]
bulk_response = API.get_bulk_device(device_ids)
for device in bulk_response.data:
    state = device['state']
    date_offline = device['date_offline']
    if state == "Offline" and date_offline:
        # Sometimes date_offline can be None
        dt = datetime.strptime(date_offline, "%Y-%m-%dT%H:%M:%S.%f")
        if dt < before:
            detailed_devices.append(device)

for device in detailed_devices:
    print("{} - {} - {}".format(device['host_name'], device['date_offline'], device['state']))

print()
print("Found {} Stale Devices".format(len(detailed_devices)))