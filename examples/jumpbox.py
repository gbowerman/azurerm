# program to create a jumpbox VM in an existing VNET for diagnostic purposes, e.g. ssh to local VMs
# uses Managed Disks, assumes first subnet in VNET has room, uses CoreOs (change code if needed)
# Arguments:
# --vmname [resource names are defaulted from this]
# --rgname 
# --user [optional, defaults to azure]
# --location [optional, defaults to VNET location]
# --vnet [optional vnet name, otherwise first vnet in resource group is picked]
# --dns [optional unique DNS name, otherwise uses vmname + 'dns'
# --password/--sshkey/--sshpath [optional pick an authentication method, 
#             otherwise if no .ssh/id_rsa.pub found will create a password for you]
# --nowait [optional to not wait for VM to be successfully provisioned]
import argparse
import azurerm
import json
from haikunator import Haikunator
import os
from os.path import expanduser
import sys
import time

# validate command line arguments
argParser = argparse.ArgumentParser()

argParser.add_argument('--vmname', '-n', required=True, action='store', help='Name')
argParser.add_argument('--rgname', '-g', required=True, action='store', help='Resource Group Name')
argParser.add_argument('--user', '-u', required=False, action='store', help='Optional username')
argParser.add_argument('--password', '-p', required=False, action='store', help='Optional password')
argParser.add_argument('--sshkey', '-k', required=False, action='store', help='SSH public key')
argParser.add_argument('--sshpath', '-s', required=False, action='store', help='SSH public key file path')
argParser.add_argument('--location', '-l', required=False, action='store', help='Location, e.g. eastus')
argParser.add_argument('--dns', '-d', required=False, action='store', help='DNS, e.g. myuniquename')
argParser.add_argument('--vnet', required=False, action='store', help='Optional VNET Name (otherwise first VNET in resource group is used)')
argParser.add_argument('--nowait', action='store_true', default=False, help='Do not wait for VM to finish provisioning')
argParser.add_argument('--verbose', '-v', action='store_true', default=False, help='Print operational details')

args = argParser.parse_args()

name = args.vmname
rgname = args.rgname
vnet = args.vnet
location = args.location
username = args.user
password = args.password
sshkey = args.sshkey
sshpath = args.sshpath
verbose = args.verbose
dns_label = args.dns
no_wait = args.nowait

# do some validation of the command line arguments to make sure all authentication scenarios are handled
if username is None:
    print('Setting username to: azure')
    username = 'azure'

if sshkey is not None and sshpath is not None:
    sys.exit('Error: You can provide an SSH public key, or a public key file path, not both.')
if password is not None and (sshkey is not None or sshpath is not None):
    sys.exit('Error: provide a password or SSH key (or nothing), not both')

use_password = False
if password is not None:
    use_password = True
else:
    if sshkey is None and sshpath is None: # no auth parameters were provided
        # look for ~/id_rsa.pub
        home = expanduser('~')
        sshpath = home + os.sep + '.ssh' + os.sep + 'id_rsa.pub'
        if os.path.isfile(sshpath) is False:
            print('Default public key file not found.')
            use_password = True
            password = Haikunator().haikunate(delimiter=',') # creates random password
            print('Created new password = ' + password)
        else:
            print('Default public key file found')

if use_password is False:
    print('Reading public key..')
    if sshkey is None:
        # at this point sshpath should have a valid Value
        with open(sshpath, 'r') as pub_ssh_file_fd:
            sshkey = pub_ssh_file_fd.read()
    
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

# authenticate
access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

# get VNET 
print('Getting VNet')
if vnet is None:
    # get first VNET in resource group
    vnets = azurerm.list_vnets_rg(access_token, subscription_id, rgname)
    # print(json.dumps(vnets, sort_keys=False, indent=2, separators=(',', ': ')))
    vnetresource = vnets['value'][0]
else:
    vnetresource = azurerm.get_vnet(access_token, subscription_id, rgname, vnet)
subnet_id = vnetresource['properties']['subnets'][0]['id']
if verbose is True:
    print('subnet_id = ' + subnet_id)

# if no location parameter was specified now would be a good time to figure out the location
if location is None:
    location = vnetresource['location']
    print('location = ' + location)

# create public IP address
public_ip_name = name + 'ip'
if dns_label is None:
    dns_label = name + 'dns'

print('Creating public ipaddr')
rmreturn = azurerm.create_public_ip(access_token, subscription_id, rgname, public_ip_name, dns_label, location)
if rmreturn.status_code != 201:
    print(rmreturn.text)
    sys.exit('Error: ' + str(rmreturn.status_code) + ' from azurerm.create_public_ip()')
ip_id = rmreturn.json()['id']
if verbose is True:
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
#publisher = 'CoreOS'
#offer = 'CoreOS'
#sku = 'Stable'
publisher = 'Canonical'
offer = 'UbuntuServer'
sku = '16.04-LTS'
version = 'latest'

print('Creating VM: ' + vm_name)
if use_password == True:
    rmreturn = azurerm.create_vm(access_token, subscription_id, rgname, vm_name, vm_size, publisher, offer, sku,
                             version, nic_id, location, username=username, password=password)
else:
    rmreturn = azurerm.create_vm(access_token, subscription_id, rgname, vm_name, vm_size, publisher, offer, sku,
                             version, nic_id, location, username=username, public_key = sshkey)
print(rmreturn)
if no_wait == False:
    print('Waiting for VM provisioning..')
    waiting = True
    while waiting:
        vm = azurerm.get_vm(access_token, subscription_id, rgname, vm_name)
        if vm['properties']['provisioningState'] == 'Succeeded':
            waiting = False
        time.sleep(5)
    print('VM provisioning complete.')
print('Connect with:')
print('ssh ' + dns_label + '.' + location + '.cloudapp.azure.com -l ' + username)
