#!/usr/bin/env python

"""
Copyright (c) 2016, Guy Bowerman
Description: Simple Azure Resource Manager Python library
License: MIT (see LICENSE.txt file for details)
"""

# networkrp.py - azurerm functions for the Microsoft.Network resource provider

from .settings import azure_rm_endpoint, NETWORK_API
from .restfns import do_delete, do_get, do_put, do_post

# list_vnets(access_token, subscription_id)
# list the VNETs in a subscription	
def list_vnets(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
						'/subscriptions/', subscription_id,
						'/providers/Microsoft.Network/',
						'/virtualNetworks?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)

# list_load_balancers(access_token, subscription_id)
# list the load balancers in a subscription	
def list_load_balancers(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
						'/subscriptions/', subscription_id,
						'/providers/Microsoft.Network/',
						'/loadBalancers?api-version=', NETWORK_API])
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

