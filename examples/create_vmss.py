'''create_vmss.py - simple program to do an imperative VMSS quick create from a platform image'''
import argparse
import json
import sys

import azurerm
from haikunator import Haikunator


def main():
    '''Main routine.'''
    # validate command line arguments
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--name', '-n', required=True,
                            action='store', help='Name of vmss')
    arg_parser.add_argument('--capacity', '-c', required=True, action='store',
                            help='Number of VMs')
    arg_parser.add_argument('--location', '-l', action='store', help='Location, e.g. eastus')
    arg_parser.add_argument('--verbose', '-v', action='store_true', default=False,
                            help='Print operational details')

    args = arg_parser.parse_args()

    name = args.name
    location = args.location
    capacity = args.capacity

    # Load Azure app defaults
    try:
        with open('azurermconfig.json') as config_file:
            config_data = json.load(config_file)
    except FileNotFoundError:
        print("Error: Expecting azurermconfig.json in current folder")
        sys.exit()

    tenant_id = config_data['tenantId']
    app_id = config_data['appId']
    app_secret = config_data['appSecret']
    subscription_id = config_data['subscriptionId']

    # authenticate
    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    # create resource group
    print('Creating resource group: ' + name)
    rmreturn = azurerm.create_resource_group(
        access_token, subscription_id, name, location)
    print(rmreturn)

    # create NSG
    nsg_name = name + 'nsg'
    print('Creating NSG: ' + nsg_name)
    rmreturn = azurerm.create_nsg(
        access_token, subscription_id, name, nsg_name, location)
    nsg_id = rmreturn.json()['id']
    print('nsg_id = ' + nsg_id)

    # create NSG rule
    nsg_rule = 'ssh'
    print('Creating NSG rule: ' + nsg_rule)
    rmreturn = azurerm.create_nsg_rule(access_token, subscription_id, name, nsg_name, nsg_rule,
                                       description='ssh rule', destination_range='22')
    #print(json.dumps(rmreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))

    # create VNET
    vnetname = name + 'vnet'
    print('Creating VNet: ' + vnetname)
    rmreturn = azurerm.create_vnet(access_token, subscription_id, name, vnetname, location,
                                   nsg_id=nsg_id)
    print(rmreturn)
    # print(json.dumps(rmreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))
    subnet_id = rmreturn.json()['properties']['subnets'][0]['id']
    print('subnet_id = ' + subnet_id)

    # create public IP address
    public_ip_name = name + 'ip'
    dns_label = name + 'ip'
    print('Creating public IP address: ' + public_ip_name)
    rmreturn = azurerm.create_public_ip(access_token, subscription_id, name, public_ip_name,
                                        dns_label, location)
    print(rmreturn)
    ip_id = rmreturn.json()['id']
    print('ip_id = ' + ip_id)

    # create load balancer with nat pool
    lb_name = vnetname + 'lb'
    print('Creating load balancer with nat pool: ' + lb_name)
    rmreturn = azurerm.create_lb_with_nat_pool(access_token, subscription_id, name, lb_name,
                                               ip_id, '50000', '50100', '22', location)
    be_pool_id = rmreturn.json()['properties']['backendAddressPools'][0]['id']
    lb_pool_id = rmreturn.json()['properties']['inboundNatPools'][0]['id']

    # create VMSS
    vmss_name = name
    vm_size = 'Standard_D1_v2'
    publisher = 'Canonical'
    offer = 'UbuntuServer'
    sku = '16.04-LTS'
    version = 'latest'
    username = 'azure'
    password = Haikunator().haikunate(delimiter=',')  # creates random password
    print('Password = ' + password)
    print('Creating VMSS: ' + vmss_name)
    rmreturn = azurerm.create_vmss(access_token, subscription_id, name, vmss_name, vm_size,
                                   capacity, publisher, offer, sku, version, subnet_id, be_pool_id,
                                   lb_pool_id, location, username=username, password=password)
    print(rmreturn)
    print(json.dumps(rmreturn.json(), sort_keys=False,
                     indent=2, separators=(',', ': ')))


if __name__ == "__main__":
    main()
