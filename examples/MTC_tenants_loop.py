# Simple example to read creds file, connect to MTC API, get access to each managed
# tenant and list a count of devices w/o Optics
# A change in comments will list each Venue Tenant ID, Device Name and Device ID

##################################################################################
# USAGE
#
##################################################################################
from __future__ import print_function
import json
from pprint import pprint
from cyapi.cyapi import CyAPI, debug_level
import argparse
import time

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

""" Optional Health Check that the server is up and running
This is a non-authenticated health-check, but returns a
CYApi APIResonse Object
"""

conn_health = API.get_mtc_health_check()
if conn_health.is_success:
    print(conn_health.data)
    print("The MTC API Connection is ready!\n")
else:
    print("MTC API Connection failed health-check.\n\nStatus Code:{}\n{} Exiting..".format(conn_health.status_code,
                                                                                        conn_health.errors))
    exit()




API.create_conn()

tenant_list = []
tenants = API.get_tenants()

print("Collecting Access to {} tenants.".format(len(tenants.data['listData'])))
# Collect the MTC Tenants, for the venueTenantId to call for tenant jwt bearer token.
for t in tenants.data['listData']:
    app = API.get_tenant_app(t['venueTenantId'])
    t['jwt'] = app.data
    tenant_list.append(t)

print("Starting Tenant Loops")
# Set the tenant_app switch and send in the jwt to create the tenant CyAPI object for access to tenant API.
# Loop each tenant and output the number of Protect Devices for each tenant.
total_no_optics = 0
total_devices = 0
#header = "VenueTenantID,Device,DeviceID"
header = "Tenant, Devices w/o Optics, Total Devices"
print(header)
for t in tenant_list:
    tenant_args = {}
    tenant_args['region'] = "NA"
    tenant_args['tenant_app'] = True
    tenant_args['tenant_jwt'] = t['jwt']

    APITenant = CyAPI(**tenant_args)
    APITenant.create_conn()

    # Get Devices Extended and then parse for Devices w/o Optics
    resp = APITenant.get_devices_extended()
    look_for = "optics"
    d_cnt = 0       # Devices counted
    no_optics = 0   # Devices w/o Optics
    for r in resp.data:
        if len(list(filter(lambda x: x.get('name') == look_for, r['products']))) == 0:
            no_optics = no_optics + 1
            #print("{},{},{}".format(t.get('venueTenantId'),r.get('name'),r.get('id')))
        d_cnt = d_cnt + 1

    print("{} : {} of {}".format(t.get('name'),no_optics, d_cnt))
    total_no_optics = total_no_optics + no_optics
    total_devices = total_devices + d_cnt
print("{} Tenants with {} devices w/ {} missing Optics.".format(len(tenant_list),total_devices,total_no_optics))

