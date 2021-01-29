# Simple example to read creds file, connect to the MTC (Multi Tenant Console) API,
# and print tenant list.

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

    parser = argparse.ArgumentParser(description='Simple example to build from', add_help=True)
    parser.add_argument('-v', '--verbose', action="count", default=0, dest="debug_level",
                        help='Show process location, comments and api responses')
    parser.add_argument('-tid', '--tid_val', help='Tenant Unique Identifier')
    parser.add_argument('-aid', '--app_id', help='Application Unique Identifier')
    parser.add_argument('-ase', '--app_secret', help='Application Secret')
    parser.add_argument('-c', '--creds_file', dest='creds', help='Path to JSON File with API info provided')
    parser.add_argument('-r', '--region', dest='region', help=regions_help, choices=regions, default='NA')
    parser.add_argument('-m', '--mtc', dest='mtc', help='Indicates API connection via MTC', default=False, action='store_true')

    return parser

commandline = ParseArgs()
args = commandline.parse_args()

if args.debug_level:
    debug_level = args.debug_level

if args.creds:
    with open(args.creds, 'rb') as f:
        creds = json.loads(f.read())

    if not creds.get('region'):
        creds['region'] = args.region

    if not creds.get('mtc'):
        creds['mtc'] = args.mtc

    API = CyAPI(**creds)

elif args.tid_val and args.app_id and args.app_secret:
    tid_val = args.tid_val
    app_id = args.app_id
    app_secret = args.app_secret
    API = CyAPI(tid_val,app_id,app_secret,args.region,args.mtc)

else:
    print("[-] Must provide valid token information")
    exit(-1)

API.create_conn()

cnt = 0
header = "Count,ID,Name,Created\n"

tenants = API.get_tenants()

print(header)
for t in tenants.data['listData']:
    cnt = cnt+1
    print("{},{},{},{}".format(cnt,t['id'],t['name'],t['createdDateTime']))
    #print(t)
