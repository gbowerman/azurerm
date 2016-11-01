# simple program to do an imperative VM quick create from a platform image
# Arguments:
# -name [resource names are defaulted from this]
# -image
# -location [same location used for all resources]
import argparse
import azurerm
import json
from haikunator import Haikunator

# validate command line arguments
argParser = argparse.ArgumentParser()

argParser.add_argument('--name', '-n', required=True, action='store', help='Name')
argParser.add_argument('--image', '-i', required=True, action='store',
                       help='VM image name')
argParser.add_argument('--location', '-l', action='store', help='Location, e.g. eastus')
argParser.add_argument('--verbose', '-v', action='store_true', default=False, help='Print operational details')

args = argParser.parse_args()

name = args.name
image = args.image
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

# create resource group
print('Creating resource group: ' + name)
rmreturn = azurerm.create_resource_group(access_token, subscription_id, name, location)
print(rmreturn)

# create NSG
nsg_name = name + 'nsg'
print('Creating NSG: ' + nsg_name)
rmreturn = azurerm.create_nsg(access_token, subscription_id, name, nsg_name, location)
nsg_id = rmreturn.json()['id']
print('nsg_id = ' + nsg_id)

# create NSG rule
nsg_rule = 'ssh'
print('Creating NSG rule: ' + nsg_rule)
rmreturn = azurerm.create_nsg_rule(access_token, subscription_id, name, nsg_name, nsg_rule, description='ssh rule',
                                  destination_range='22')
print(rmreturn)
print(json.dumps(rmreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))

# create storage account
print('Creating storage account: ' + name)
rmreturn = azurerm.create_storage_account(access_token, subscription_id, name, name, location, storage_type='Premium_LRS')
print(rmreturn)

# create VNET
vnetname = name + 'vnet'
print('Creating VNet: ' + vnetname)
rmreturn = azurerm.create_vnet(access_token, subscription_id, name, vnetname, location, nsg_id=nsg_id)
print(rmreturn)
# print(json.dumps(rmreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))
subnet_id = rmreturn.json()['properties']['subnets'][0]['id']
print('subnet_id = ' + subnet_id)

# create public IP address
public_ip_name = name + 'ip'
dns_label = name + 'ip'
print('Creating public IP address: ' + public_ip_name)
rmreturn = azurerm.create_public_ip(access_token, subscription_id, name, public_ip_name, dns_label, location)
print(rmreturn)
ip_id = rmreturn.json()['id']
print('ip_id = ' + ip_id)

# create NIC
nic_name = name + 'nic'
print('Creating NIC: ' + nic_name)
rmreturn = azurerm.create_nic(access_token, subscription_id, name, nic_name, ip_id, subnet_id, location)
print(rmreturn)
nic_id = rmreturn.json()['id']

# create VM
vm_name = name
vm_size = 'Standard_DS1'
publisher = 'Canonical'
offer = 'UbuntuServer'
sku = '16.04.0-LTS'
version = 'latest'
os_uri = 'http://' + name + '.blob.core.windows.net/vhds/osdisk.vhd'
username = 'azure'
password = Haikunator.haikunate(delimiter=',') # creates random password

print('Creating VM: ' + vm_name)
rmreturn = azurerm.create_vm(access_token, subscription_id, name, vm_name, vm_size, publisher, offer, sku,
                             version, name, os_uri, nic_id, location, username=username, password=password)
print(rmreturn)
print(json.dumps(rmreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))
