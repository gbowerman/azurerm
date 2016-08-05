"""
Copyright (c) 2016, Guy Bowerman
Description: Simple Azure Resource Manager Python library
License: MIT (see LICENSE.txt file for details)
"""

# networkrp.py - azurerm functions for the Microsoft.Network resource provider
from .restfns import do_get, do_put
from .settings import azure_rm_endpoint, NETWORK_API


# list_vnets(access_token, subscription_id)
# list the VNETs in a subscription	
def list_vnets(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Network/',
                        '/virtualNetworks?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)

# create_vnet(access_token, subscription_id, resource_group, location, name)
# create a VNet with specified name and location. Default the adress prefixes for now.
def create_vnet(access_token, subscription_id, resource_group, name, location):
    endpoint = ''.join([azure_rm_endpoint,
                    '/subscriptions/', subscription_id,
                    '/resourceGroups/', resource_group,
                    '/providers/Microsoft.Network/virtualNetworks/', name,
                    '?api-version=', NETWORK_API])
    body = ''.join(['{   "location": "', location, '", "properties": ',
                    '{"addressSpace": {"addressPrefixes": ["10.0.0.0/16"]}, ',
                    '"subnets": [ { "name": "subnet", "properties": { "addressPrefix": "10.0.0.0/16" }}]}}'])
    return do_put(endpoint, body, access_token)

# create_nic(access_token, subscription_id, resource_group, nic_name, public_ip_id, subnet_id, location)
# create a network interface with an assoicated public ip address
def create_nic(access_token, subscription_id, resource_group, nic_name, public_ip_id, subnet_id, location):
    endpoint = ''.join([azure_rm_endpoint,
                    '/subscriptions/', subscription_id,
                    '/resourceGroups/', resource_group,
                    '/providers/Microsoft.Network/networkInterfaces/', nic_name,
                    '?api-version=', NETWORK_API])
    body = ''.join(['{ "location": "', location,
                    '", "properties": { "ipConfigurations": [{ "name": "ipconfig1", "properties": {',
                    '"privateIPAllocationMethod": "Dynamic", "publicIPAddress": {',
                    '"id": "', public_ip_id,
                    '" }, "subnet": { "id": "', subnet_id,
                    '" } } } ] } }'])
    return do_put(endpoint, body, access_token)


# list_nics(access_token, subscription_id)
# list the network interfaces in a subscription
def list_nics(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Network/',
                        '/networkInterfaces?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


# list_nics_rg(access_token, subscription_id, resource_group)
# list network interface cards within a resource group	
def list_nics_rg(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/',
                        '/networkInterfaces?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


# list_load_balancers(access_token, subscription_id)
# list the load balancers in a subscription	
def list_load_balancers(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Network/',
                        '/loadBalancers?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


# list_load_balancers_rg(access_token, subscription_id, resource_group)
# list the load balancers in a resource group	
def list_load_balancers_rg(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/',
                        '/loadBalancers?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


# get_load_balancer(access_token, subscription_id, resource_group, lb_name)
# get details about a load balancer	
def get_load_balancer(access_token, subscription_id, resource_group, lb_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/',
                        '/loadBalancers/', lb_name,
                        '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


# list_public_ips(access_token, subscription_id, resource_group)
# list the public ip addresses in a resource group	
def list_public_ips(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/',
                        'publicIPAddresses?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)

# create_public_ip(access_token, subscription_id, resource_group)
# list the public ip addresses in a resource group
def create_public_ip(access_token, subscription_id, resource_group, public_ip_name, dns_label, location):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/publicIPAddresses/', public_ip_name,
                        '?api-version=', NETWORK_API])
    body = ''.join(['{"location": "', location,
                    '", "properties": {"publicIPAllocationMethod": "Dynamic", "dnsSettings": {',
                    '"domainNameLabel": "', dns_label, '"}}}'])
    return do_put(endpoint, body, access_token)

# get_public_ip(access_token, subscription_id, resource_group)
# get details about the named public ip address
def get_public_ip(access_token, subscription_id, resource_group, ip_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/',
                        'publicIPAddresses/', ip_name,
                        '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


# get_network_usage(access_token, subscription_id, location)
# list network usage and limits for a location
def get_network_usage(access_token, subscription_id, location):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Network/locations/', location,
                        '/usages?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)
