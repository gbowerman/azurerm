# simple program to do an imperative VMSS quick create from a platform image
# Arguments:
# -name [resource names are defaulted from this]
# -image
# -location [same location used for all resources]
import argparse
import azurerm
import json
from random import choice
from string import ascii_lowercase
from haikunator import Haikunator

# validate command line arguments
argParser = argparse.ArgumentParser()

argParser.add_argument('--name', '-n', required=True, action='store', help='Name of vmss')
argParser.add_argument('--capacity', '-c', required=True, action='store',
                       help='Number of VMs')
argParser.add_argument('--location', '-l', action='store', help='Location, e.g. eastus')
argParser.add_argument('--verbose', '-v', action='store_true', default=False, help='Print operational details')

args = argParser.parse_args()

name = args.name
location = args.location
capacity = args.capacity

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
rmreturn = azurerm.create_nsg_rule(access_token, subscription_id, name, nsg_name, nsg_rule, \
    description='ssh rule', destination_range='22')
#print(json.dumps(rmreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))

# create VNET
vnetname = name + 'vnet'
print('Creating VNet: ' + vnetname)
rmreturn = azurerm.create_vnet(access_token, subscription_id, name, vnetname, location, \
    nsg_id=nsg_id)
print(rmreturn)
# print(json.dumps(rmreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))
subnet_id = rmreturn.json()['properties']['subnets'][0]['id']
print('subnet_id = ' + subnet_id)

# create public IP address
public_ip_name = name + 'ip'
dns_label = name + 'ip'
print('Creating public IP address: ' + public_ip_name)
rmreturn = azurerm.create_public_ip(access_token, subscription_id, name, public_ip_name, \
    dns_label, location)
print(rmreturn)
ip_id = rmreturn.json()['id']
print('ip_id = ' + ip_id)

# create load balancer with nat pool
lb_name = vnetname + 'lb'
print('Creating load balancer with nat pool: ' + lb_name)
rmreturn = azurerm.create_lb_with_nat_pool(access_token, subscription_id, name, lb_name, ip_id, \
    '50000', '50100', '22', location)
be_pool_id = rmreturn.json()['properties']['backendAddressPools'][0]['id']
lb_pool_id = rmreturn.json()['properties']['inboundNatPools'][0]['id']

# create VMSS
vmss_name = name
vm_size = 'Standard_A1'
publisher = 'Canonical'
offer = 'UbuntuServer'
sku = '16.04-LTS'
version = 'latest'
username = 'azure'
password = Haikunator().haikunate(delimiter=',') # creates random password
print('Password = ' + password)
print('Creating VMSS: ' + vmss_name)
rmreturn = azurerm.create_vmss(access_token, subscription_id, name, vmss_name, vm_size, capacity, \
    publisher, offer, sku, version, subnet_id, be_pool_id, lb_pool_id, location, \
    username=username, password=password)
print(rmreturn)
print(json.dumps(rmreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))
