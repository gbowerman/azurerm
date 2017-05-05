import argparse
import azurerm
import json
import re
import sys

# validate command line arguments
argParser = argparse.ArgumentParser()

argParser.add_argument('--vmssname', '-n', required=True,
                       action='store', help='VMSS Name')
argParser.add_argument('--rgname', '-g', required=True,
                       action='store', help='Resource Group Name')
argParser.add_argument('--details', '-a', required=False,
                       action='store', help='Print all details')

args = argParser.parse_args()

name = args.vmssname
rgname = args.rgname
details = args.details

# Load Azure app defaults
try:
    with open('azurermconfig.json') as configFile:
        configData = json.load(configFile)
except FileNotFoundError:
    print("Error: Expecting azurermconfig.json in current folder")
    sys.exit()

tenant_id = configData['tenantId']
app_id = configData['appId']
app_secret = configData['appSecret']
subscription_id = configData['subscriptionId']

access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

public_ips = azurerm.get_vmss_public_ips(access_token, subscription_id, rgname, name)

if details is True:
    print(json.dumps(public_ips, sort_keys=False, indent=2, separators=(',', ': ')))
else:
    for ip in public_ips['value']:
        vm_id = re.search('Machines/(.*)/networkInt', ip['id']).group(1)
        ipaddr = ip['properties']['ipAddress']
        print('VM id: ' + vm_id + ', IP: ' + ipaddr)

