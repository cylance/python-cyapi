# Simple example to read creds file, connect to API, and print detections.

##################################################################################
# USAGE
#
##################################################################################
from __future__ import print_function
import json
from pprint import pprint
from cyapi.cyapi import CyAPI, debug_level
import argparse

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

    parser = argparse.ArgumentParser(description='Create a new OPTICS Rule Set based on an existing on and best practice phases.', add_help=True)
    parser.add_argument('-v', '--verbose', action="count", default=0, dest="debug_level",
                        help='Show process location, comments and api responses')
    # Cylance SE Tenant
    parser.add_argument('-tid', '--tid_val', help='Tenant Unique Identifier')
    parser.add_argument('-aid', '--app_id', help='Application Unique Identifier')
    parser.add_argument('-ase', '--app_secret', help='Application Secret')
    parser.add_argument('-c', '--creds_file', dest='creds', help='Path to JSON File with API info provided')
    parser.add_argument('-r', '--region', dest='region', help=regions_help, choices=regions, default='NA')

    return parser

##################################################################################
# Tenant Integration
# Modify the keys to align with your tenant API
##################################################################################
# Cylance SE Tenant
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
detections = API.get_detections()

pprint(detections)