'''networkrp.py - azurerm functions for the Microsoft.Network resource provider'''
import json
from .restfns import do_delete, do_get, do_put
from .settings import get_rm_endpoint, NETWORK_API


# create_lb_with_nat_pool(access_token, subscription_id, resource_group,
# lb_name, public_ip_id,
def create_lb_with_nat_pool(access_token, subscription_id, resource_group, lb_name, public_ip_id,
                            fe_start_port, fe_end_port, backend_port, location):
    '''Create a load balancer with inbound NAT pools.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/loadBalancers/', lb_name,
                        '?api-version=', NETWORK_API])
    lb_body = {'location': location}
    frontendipcconfig = {'name': 'LoadBalancerFrontEnd'}
    fipc_properties = {'publicIPAddress': {'id': public_ip_id}}
    frontendipcconfig['properties'] = fipc_properties
    properties = {'frontendIPConfigurations': [frontendipcconfig]}
    properties['backendAddressPools'] = [{'name': 'bepool'}]
    inbound_natpool = {'name': 'natpool'}
    lbfe_id = '/subscriptions/' + subscription_id + '/resourceGroups/' + resource_group + \
        '/providers/Microsoft.Network/loadBalancers/' + lb_name + \
        '/frontendIPConfigurations/LoadBalancerFrontEnd'
    ibnp_properties = {'frontendIPConfiguration': {'id': lbfe_id}}
    ibnp_properties['protocol'] = 'tcp'
    ibnp_properties['frontendPortRangeStart'] = fe_start_port
    ibnp_properties['frontendPortRangeEnd'] = fe_end_port
    ibnp_properties['backendPort'] = backend_port
    inbound_natpool['properties'] = ibnp_properties
    properties['inboundNatPools'] = [inbound_natpool]
    lb_body['properties'] = properties
    body = json.dumps(lb_body)
    return do_put(endpoint, body, access_token)


def create_nic(access_token, subscription_id, resource_group, nic_name, public_ip_id, subnet_id, location, nsg_id=None):
    '''Create a network interface with an associated public ip address.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/networkInterfaces/', nic_name,
                        '?api-version=', NETWORK_API])
    nic_body = {'location': location}
    ipconfig = {'name': 'ipconfig1'}
    ipc_properties = {'privateIPAllocationMethod': 'Dynamic'}
    ipc_properties['publicIPAddress'] = {'id': public_ip_id}
    ipc_properties['subnet'] = {'id': subnet_id}
    ipconfig['properties'] = ipc_properties
    properties = {'ipConfigurations': [ipconfig]}
    if nsg_id is not None:
        properties['networkSecurityGroup'] = {'id': nsg_id}
    nic_body['properties'] = properties
    body = json.dumps(nic_body)
    return do_put(endpoint, body, access_token)


def create_nsg(access_token, subscription_id, resource_group, nsg_name, location):
    '''Create network security group (use create_nsg_rule() to add rules to it).
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/networkSecurityGroups/', nsg_name,
                        '?api-version=', NETWORK_API])
    nsg_body = {'location': location}
    body = json.dumps(nsg_body)
    return do_put(endpoint, body, access_token)


# create_nsg_rule(access_token, subscription_id, resource_group, nsg_name, nsg_rule_name,
# description, protocol='Tcp', source_range='*', destination_range='*',
# source_prefix='*',
def create_nsg_rule(access_token, subscription_id, resource_group, nsg_name, nsg_rule_name, description, protocol='Tcp', source_range='*', destination_range='*', source_prefix='*', destination_prefix='*', access='Allow', priority=100, direction='Inbound'):
    '''Create network security group rule.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/networkSecurityGroups/', nsg_name,
                        '/securityRules/', nsg_rule_name,
                        '?api-version=', NETWORK_API])
    properties = {'description': description}
    properties['protocol'] = protocol
    properties['sourcePortRange'] = source_range
    properties['destinationPortRange'] = destination_range
    properties['sourceAddressPrefix'] = source_prefix
    properties['destinationAddressPrefix'] = destination_prefix
    properties['access'] = access
    properties['priority'] = priority
    properties['direction'] = direction
    ip_body = {'properties': properties}
    body = json.dumps(ip_body)
    return do_put(endpoint, body, access_token)


def create_public_ip(access_token, subscription_id, resource_group, public_ip_name, dns_label, location):
    '''Create a public ip address.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/publicIPAddresses/', public_ip_name,
                        '?api-version=', NETWORK_API])
    ip_body = {'location': location}
    properties = {'publicIPAllocationMethod': 'Dynamic'}
    properties['dnsSettings'] = {'domainNameLabel': dns_label}
    ip_body['properties'] = properties
    body = json.dumps(ip_body)
    return do_put(endpoint, body, access_token)


# create_vnet(access_token, subscription_id, resource_group, name, location,
def create_vnet(access_token, subscription_id, resource_group, name, location,
                address_prefix='10.0.0.0/16', subnet_prefix='10.0.0.0/16', nsg_id=None):
    '''Create a VNet with specified name and location. Optional subnet address prefix..
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/virtualNetworks/', name,
                        '?api-version=', NETWORK_API])

    vnet_body = {'location': location}
    properties = {'addressSpace': {'addressPrefixes': [address_prefix]}}
    subnet = {'name': 'subnet'}
    subnet['properties'] = {'addressPrefix': subnet_prefix}
    if nsg_id is not None:
        subnet['properties']['networkSecurityGroup'] = {'id': nsg_id}
    properties['subnets'] = [subnet]
    vnet_body['properties'] = properties
    body = json.dumps(vnet_body)
    return do_put(endpoint, body, access_token)


def delete_load_balancer(access_token, subscription_id, resource_group, lb_name):
    '''Delete a load balancer.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/loadBalancers/', lb_name,
                        '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


def delete_nic(access_token, subscription_id, resource_group, nic_name):
    '''Delete a network interface.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/networkInterfaces/', nic_name,
                        '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


def delete_nsg(access_token, subscription_id, resource_group, nsg_name):
    '''Delete network security group.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/networkSecurityGroups/', nsg_name,
                        '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


def delete_nsg_rule(access_token, subscription_id, resource_group, nsg_name, nsg_rule_name):
    '''Delete network security group rule.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/networkSecurityGroups/', nsg_name,
                        '/securityRules/', nsg_rule_name,
                        '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


def delete_public_ip(access_token, subscription_id, resource_group, public_ip_name):
    '''Delete a public ip addresses associated with a resource group.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/publicIPAddresses/', public_ip_name,
                        '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


def delete_vnet(access_token, subscription_id, resource_group, name):
    '''Delete a virtual network.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/virtualNetworks/', name,
                        '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


def get_lb_nat_rule(access_token, subscription_id, resource_group, lb_name, rule_name):
    '''Get details about a load balancer inbound NAT rule.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/loadBalancers/', lb_name,
                        '/inboundNatRules/', rule_name,
                        '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def get_load_balancer(access_token, subscription_id, resource_group, lb_name):
    '''Get details about a load balancer	.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/loadBalancers/', lb_name,
                        '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def get_network_usage(access_token, subscription_id, location):
    '''List network usage and limits for a location.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Network/locations/', location,
                        '/usages?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def get_nic(access_token, subscription_id, resource_group, nic_name):
    '''Get details about a network interface.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/networkInterfaces/', nic_name,
                        '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def get_public_ip(access_token, subscription_id, resource_group, ip_name):
    '''Get details about the named public ip address.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/',
                        'publicIPAddresses/', ip_name,
                        '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def get_vnet(access_token, subscription_id, resource_group, vnet_name):
    '''Get details about the named virtual network.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/virtualNetworks/', vnet_name,
                        '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_lb_nat_rules(access_token, subscription_id, resource_group, lb_name):
    '''List the inbound NAT rules for a load balancer.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/loadBalancers/', lb_name,
                        'inboundNatRules?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_load_balancers(access_token, subscription_id):
    '''List the load balancers in a subscription	.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Network/',
                        '/loadBalancers?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_load_balancers_rg(access_token, subscription_id, resource_group):
    '''List the load balancers in a resource group	.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/',
                        '/loadBalancers?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_nics(access_token, subscription_id):
    '''List the network interfaces in a subscription.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Network/',
                        '/networkInterfaces?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_nics_rg(access_token, subscription_id, resource_group):
    '''List network interface cards within a resource group	.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/',
                        '/networkInterfaces?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_public_ips(access_token, subscription_id, resource_group):
    '''List the public ip addresses in a resource group	.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/',
                        'publicIPAddresses?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_vnets(access_token, subscription_id):
    '''List the VNETs in a subscription	.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Network/',
                        '/virtualNetworks?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_vnets_rg(access_token, subscription_id, resource_group):
    '''List the VNETs in a resource group.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/',
                        '/virtualNetworks?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def update_load_balancer(access_token, subscription_id, resource_group, lb_name, body):
    '''Updates a load balancer model, i.e. PUT an updated LB body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/loadBalancers/', lb_name,
                        '?api-version=', NETWORK_API])
    return do_put(endpoint, body, access_token)
