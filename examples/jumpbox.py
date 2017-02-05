# program to create a jumpbox VM in an existing VNET for diagnostic purposes, e.g. ssh to local VMs
# uses Managed Disks, assumes first subnet in VNET has room, uses CoreOs (change code if needed)
# Arguments:
# --name [resource names are defaulted from this]
# --image
# --location [same location used for all resources]
# --vnet optional vnet name, otherwise first vnet in resource group is picked
import argparse
import azurerm
import json
from haikunator import Haikunator
import sys
import time

# validate command line arguments
argParser = argparse.ArgumentParser()

argParser.add_argument('--name', '-n', required=True, action='store', help='Name')
argParser.add_argument('--rgname', '-g', required=True, action='store', help='Resource Group Name')
argParser.add_argument('--vnet', required=False, action='store', help='Optional VNET Name (otherwise first VNET in resource group is used)')
argParser.add_argument('--location', '-l', required=True, action='store', help='Location, e.g. eastus')
argParser.add_argument('--verbose', '-v', action='store_true', default=False, help='Print operational details')

args = argParser.parse_args()

name = args.name
rgname = args.rgname
vnet = args.vnet
location = args.location

# Load Azure app defaults
try:
   with open('azurermconfig.json') as configFile:    
      configData = json.load(configFile)
except FileNotFoundError:
   print("Error: Expecting vmssConfig.json in current folder")
   sys.exit()
   
tenant_id = configData['tenantId']
app_id = configData['appId']
app_secret = configData['appSecret']
subscription_id = configData['subscriptionId']

# authenticate
access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

# initialize haikunator
h = Haikunator()

# get VNET 
print('Getting VNet')
if vnet is None:
    # get first VNET in resource group
    vnets = azurerm.list_vnets_rg(access_token, subscription_id, rgname)
    #print(json.dumps(vnets, sort_keys=False, indent=2, separators=(',', ': ')))
    vnetresource = vnets['value'][0]
else:
    vnetresource = azurerm.get_vnet(access_token, subscription_id, rgname, vnet)
subnet_id = vnetresource['properties']['subnets'][0]['id']
print('subnet_id = ' + subnet_id)

# create public IP address
public_ip_name = name + 'ip'
dns_label = name + 'ip'
print('Creating public IP address: ' + public_ip_name)
rmreturn = azurerm.create_public_ip(access_token, subscription_id, rgname, public_ip_name, dns_label, location)
print(rmreturn)
ip_id = rmreturn.json()['id']
print('ip_id = ' + ip_id)

print('Waiting for IP provisioning..')
waiting = True
while waiting:
    ip = azurerm.get_public_ip(access_token, subscription_id, rgname, public_ip_name)
    if ip['properties']['provisioningState'] == 'Succeeded':
        waiting = False
    time.sleep(1)

# create NIC
nic_name = name + 'nic'
print('Creating NIC: ' + nic_name)
rmreturn = azurerm.create_nic(access_token, subscription_id, rgname, nic_name, ip_id, subnet_id, location)
#print(json.dumps(rmreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))
nic_id = rmreturn.json()['id']

print('Waiting for NIC provisioning..')
waiting = True
while waiting:
    nic = azurerm.get_nic(access_token, subscription_id, rgname, nic_name)
    if nic['properties']['provisioningState'] == 'Succeeded':
        waiting = False
    time.sleep(1)

# create VM
vm_name = name
vm_size = 'Standard_D1'
publisher = 'CoreOS'
offer = 'CoreOS'
sku = 'Stable'
version = 'latest'
os_uri = 'http://' + name + '.blob.core.windows.net/vhds/' + name + 'osdisk.vhd'
username = 'azure'
password = h.haikunate(delimiter=',') # creates random password
print('password = ' + password)
print('Creating VM: ' + vm_name)
rmreturn = azurerm.create_vm(access_token, subscription_id, rgname, vm_name, vm_size, publisher, offer, sku,
                             version, nic_id, location, username=username, password=password)
print(rmreturn)
#print(json.dumps(rmreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))
