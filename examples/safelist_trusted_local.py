# Simple example to read creds file, connect to API, and print Trusted Local
#  threats found in your environment.
#  Using the --Force argument will add these threats to your Global Safe List

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

    parser = argparse.ArgumentParser(description='Safelist all Trusted Local detections. See -F flag', add_help=True)
    parser.add_argument('-v', '--verbose', action="count", default=0, dest="debug_level",
                        help='Show process location, comments and api responses')
    parser.add_argument('-tid', '--tid_val', help='Tenant Unique Identifier')
    parser.add_argument('-aid', '--app_id', help='Application Unique Identifier')
    parser.add_argument('-ase', '--app_secret', help='Application Secret')
    parser.add_argument('-c', '--creds_file', dest='creds', help='Path to JSON File with API info provided')
    parser.add_argument('-r', '--region', dest='region', help=regions_help, choices=regions, default='NA')
    parser.add_argument('-F', '--Force', dest='force', help='Perform the Global Safelisting action, otherwise it will just list', action="store_true")

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

if not args.force:
    print("[+] Listing all Trusted Local threats in your environment")
else:
    print("[+] Globally Safelisting all Trusted Local threats in your environment")

API.create_conn()
threats = API.get_threats()
tl_threats = []
for threat in threats:
    if "Trusted" == threat.get('classification') and "Local" == threat.get('sub_classification'):
        tl_threats.append(threat)

for threat in tl_threats:
    if args.force:
        API.add_to_global_list("safe", "Trusted Local", threat.get('sha256'))
    else:
        pprint(threat)