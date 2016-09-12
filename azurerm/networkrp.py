# networkrp.py - azurerm functions for the Microsoft.Network resource provider
from .restfns import do_delete, do_get, do_put
from .settings import azure_rm_endpoint, NETWORK_API


# create_nic(access_token, subscription_id, resource_group, nic_name, public_ip_id, subnet_id, location)
# create a network interface with an associated public ip address
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

	
# create_nsg(access_token, subscription_id, resource_group, nsg_name, location)
# create network security group (use create_nsg_rule() to add rules to it)
def create_nsg(access_token, subscription_id, resource_group, nsg_name, location):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/networkSecurityGroups/', nsg_name,
                        '?api-version=', NETWORK_API])
    body = ''.join(['{ "location":"', location, '" }'])
    return do_put(endpoint, body, access_token)


# create_nsg_rule(access_token, subscription_id, resource_group, nsg_name, nsg_rule_name, description, protocol='Tcp', source_range='*', destination_range='*', source_prefix='Internet', destination_prefix='*', access = 'Allow', priority=100, direction='Inbound')
# create network security group rule
def create_nsg_rule(access_token, subscription_id, resource_group, nsg_name, nsg_rule_name, description, protocol='Tcp', source_range='*', destination_range='*', source_prefix='Internet', destination_prefix='*', access = 'Allow', priority=100, direction='Inbound'):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/networkSecurityGroups/', nsg_name,
                        '/securityRules/', nsg_rule_name,
                        '?api-version=', NETWORK_API])
    body = ''.join(['{ "properties":{ "description":"', description, 
                        '", "protocol":"', protocol, 
                        '", "sourcePortRange":"', source_range, 
                        '", "destinationPortRange":"', destination_range, 
                        '", "sourceAddressPrefix": "', source_prefix, 
                        '", "destinationAddressPrefix": "', destination_prefix,
                        '", "sourceAddressPrefix":"*", "destinationAddressPrefix":"*", "access":"', access, 
                        '", "priority":', str(priority), 
                        ', "direction":"', direction, '" }}'])
    return do_put(endpoint, body, access_token)


# create_public_ip(access_token, subscription_id, resource_group, public_ip_name, dns_label, location)
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


# create_vnet(access_token, subscription_id, resource_group, name, location, address_prefix='10.0.0.0/16', nsg_id=None))
# create a VNet with specified name and location. Optional subnet address prefix.
def create_vnet(access_token, subscription_id, resource_group, name, location, address_prefix='10.0.0.0/16', nsg_id=None):
    endpoint = ''.join([azure_rm_endpoint,
                    '/subscriptions/', subscription_id,
                    '/resourceGroups/', resource_group,
                    '/providers/Microsoft.Network/virtualNetworks/', name,
                    '?api-version=', NETWORK_API])
    if nsg_id is not None:
        nsg_reference = ''.join([', "networkSecurityGroup": { "id": "',nsg_id,'"} '])
    else:
        nsg_reference = ''	
    body = ''.join(['{   "location": "', location, '", "properties": ',
                    '{"addressSpace": {"addressPrefixes": ["', address_prefix, '"]}, ',
                    '"subnets": [ { "name": "subnet", "properties": { "addressPrefix": "', address_prefix, 
                    '"', nsg_reference, '}}]}}'])
    return do_put(endpoint, body, access_token)


# delete_nic(access_token, subscription_id, resource_group, nic_name)
# delete a network interface
def delete_nic(access_token, subscription_id, resource_group, nic_name):
    endpoint = ''.join([azure_rm_endpoint,
                    '/subscriptions/', subscription_id,
                    '/resourceGroups/', resource_group,
                    '/providers/Microsoft.Network/networkInterfaces/', nic_name,
                    '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)

	
# delete_nsg(access_token, subscription_id, resource_group, nsg_name)
# delete network security group
def delete_nsg(access_token, subscription_id, resource_group, nsg_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/networkSecurityGroups/', nsg_name,
                        '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


# delete_nsg_rule(access_token, subscription_id, resource_group, nsg_name, nsg_rule_name)
# delete network security group rule
def delete_nsg_rule(access_token, subscription_id, resource_group, nsg_name, nsg_rule_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/networkSecurityGroups/', nsg_name,
                        '/securityRules/', nsg_rule_name,
                        '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


# delete_public_ip(access_token, subscription_id, resource_group, public_ip_name)
# delete a public ip addresses associated with a resource group
def delete_public_ip(access_token, subscription_id, resource_group, public_ip_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/publicIPAddresses/', public_ip_name,
                        '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


# delete_vnet(access_token, subscription_id, resource_group, name)
# delete a virtual network
def delete_vnet(access_token, subscription_id, resource_group, name):
    endpoint = ''.join([azure_rm_endpoint,
                    '/subscriptions/', subscription_id,
                    '/resourceGroups/', resource_group,
                    '/providers/Microsoft.Network/virtualNetworks/', name,
                    '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)


# get_lb_nat_rule(access_token, subscription_id, resource_group, lb_name, rule_name)
# get details about a load balancer inbound NAT rule
def get_lb_nat_rule(access_token, subscription_id, resource_group, lb_name, rule_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/loadBalancers/', lb_name,
                        '/inboundNatRules/', rule_name,
                        '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)

    
# get_load_balancer(access_token, subscription_id, resource_group, lb_name)
# get details about a load balancer	
def get_load_balancer(access_token, subscription_id, resource_group, lb_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/loadBalancers/', lb_name,
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


# get_vnet(access_token, subscription_id, resource_group, vnet_name)
# get details about the named virtual network
def get_vnet(access_token, subscription_id, resource_group, vnet_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/virtualNetworks/', vnet_name,
                        '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


# list_lb_nat_rules(access_token, subscription_id, resource_group, lb_name)
# list the inbound NAT rules for a load balancer
def list_lb_nat_rules(access_token, subscription_id, resource_group, lb_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/loadBalancers/', lb_name,
                        'inboundNatRules?api-version=', NETWORK_API])
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


# list_public_ips(access_token, subscription_id, resource_group)
# list the public ip addresses in a resource group	
def list_public_ips(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/',
                        'publicIPAddresses?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


# list_vnets(access_token, subscription_id)
# list the VNETs in a subscription	
def list_vnets(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Network/',
                        '/virtualNetworks?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)