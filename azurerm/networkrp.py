'''networkrp.py - azurerm functions for the Microsoft.Network resource provider'''
import json
from .restfns import do_delete, do_get, do_put
from .settings import get_rm_endpoint, NETWORK_API


def create_lb_with_nat_pool(access_token, subscription_id, resource_group, lb_name, public_ip_id,
                            fe_start_port, fe_end_port, backend_port, location):
    '''Create a load balancer with inbound NAT pools.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        lb_name (str): Name of the new load balancer.
        public_ip_id (str): Public IP address resource id.
        fe_start_port (int): Start of front-end port range.
        fe_end_port (int): End of front-end port range.
        backend_port (int): Back end port for VMs.
        location (str): Azure data center location. E.g. westus.

    Returns:
        HTTP response. Load Balancer JSON body.
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


def create_nic(access_token, subscription_id, resource_group, nic_name, public_ip_id, subnet_id,
               location, nsg_id=None):
    '''Create a network interface with an associated public ip address.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        nic_name (str): Name of the new NIC.
        public_ip_id (str): Public IP address resource id.
        subnetid (str): Subnet resource id.
        location (str): Azure data center location. E.g. westus.
        nsg_id (str): Optional Network Secruity Group resource id.

    Returns:
        HTTP response. NIC JSON body.
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

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        nsg_name (str): Name of the new NSG.
        location (str): Azure data center location. E.g. westus.

    Returns:
        HTTP response. NSG JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/networkSecurityGroups/', nsg_name,
                        '?api-version=', NETWORK_API])
    nsg_body = {'location': location}
    body = json.dumps(nsg_body)
    return do_put(endpoint, body, access_token)


def create_nsg_rule(access_token, subscription_id, resource_group, nsg_name, nsg_rule_name,
                    description, protocol='Tcp', source_range='*', destination_range='*',
                    source_prefix='*', destination_prefix='*', access='Allow', priority=100,
                    direction='Inbound'):
    '''Create network security group rule.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        nsg_name (str): Name of the Network Security Group.
        nsg_rule_name (str): Name of the new rule.
        description (str): Description.
        protocol (str): Optional protocol. Default Tcp.
        source_range (str): Optional source IP range. Default '*'.
        destination_range (str): Destination IP range. Default *'.
        source_prefix (str): Source DNS prefix. Default '*'.
        destination_prefix (str): Destination prefix. Default '*'.
        access (str): Allow or deny rule. Default Allow.
        priority: Relative priority. Default 100.
        direction: Inbound or Outbound. Default Inbound.

    Returns:
        HTTP response. NSG JSON rule body.
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


def create_public_ip(access_token, subscription_id, resource_group, public_ip_name, dns_label,
                     location):
    '''Create a public ip address.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        public_ip_name (str): Name of the new public ip address resource.
        dns_label (str): DNS label to apply to the IP address.
        location (str): Azure data center location. E.g. westus.

    Returns:
        HTTP response. Public IP address JSON body.
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


def create_vnet(access_token, subscription_id, resource_group, name, location,
                address_prefix='10.0.0.0/16', subnet_prefix='10.0.0.0/16', nsg_id=None):
    '''Create a VNet with specified name and location. Optional subnet address prefix..

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        name (str): Name of the new VNet.
        location (str): Azure data center location. E.g. westus.
        address_prefix (str): Optional VNet address prefix. Default '10.0.0.0/16'.
        subnet_prefix (str): Optional subnet address prefix. Default '10.0.0.0/16'.
        nsg_id (str): Optional Netwrok Security Group resource Id. Default None.

    Returns:
        HTTP response. VNet JSON body.
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

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        lb_name (str): Name of the load balancer.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/loadBalancers/', lb_name,
                        '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


def delete_nic(access_token, subscription_id, resource_group, nic_name):
    '''Delete a network interface.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        nic_name (str): Name of the NIC.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/networkInterfaces/', nic_name,
                        '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


def delete_nsg(access_token, subscription_id, resource_group, nsg_name):
    '''Delete network security group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        nsg_name (str): Name of the NSG.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/networkSecurityGroups/', nsg_name,
                        '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


def delete_nsg_rule(access_token, subscription_id, resource_group, nsg_name, nsg_rule_name):
    '''Delete network security group rule.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        nsg_name (str): Name of the Network Security Group.
        nsg_rule_name (str): Name of the NSG rule.

    Returns:
        HTTP response.
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

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        public_ip_name (str): Name of the public ip address resource.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/publicIPAddresses/', public_ip_name,
                        '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


def delete_vnet(access_token, subscription_id, resource_group, name):
    '''Delete a virtual network.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        name (str): Name of the VNet.

    Returns:
        HTTP response. VNet JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/virtualNetworks/', name,
                        '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


def get_lb_nat_rule(access_token, subscription_id, resource_group, lb_name, rule_name):
    '''Get details about a load balancer inbound NAT rule.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        lb_name (str): Name of the load balancer.
        rule_name (str): Name of the NAT rule.

    Returns:
        HTTP response. JSON body of rule.
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

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        lb_name (str): Name of the load balancer.

    Returns:
        HTTP response. JSON body of load balancer properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/loadBalancers/', lb_name,
                        '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def get_network_usage(access_token, subscription_id, location):
    '''List network usage and limits for a location.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        location (str): Azure data center location. E.g. westus.

    Returns:
        HTTP response. JSON body of network usage.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Network/locations/', location,
                        '/usages?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def get_nic(access_token, subscription_id, resource_group, nic_name):
    '''Get details about a network interface.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        nic_name (str): Name of the NIC.

    Returns:
        HTTP response. NIC JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/networkInterfaces/', nic_name,
                        '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def get_public_ip(access_token, subscription_id, resource_group, ip_name):
    '''Get details about the named public ip address.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        public_ip_name (str): Name of the public ip address resource.

    Returns:
        HTTP response. Public IP address JSON body.
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

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vnet_name (str): Name of the VNet.

    Returns:
        HTTP response. VNet JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/virtualNetworks/', vnet_name,
                        '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_asgs(access_token, subscription_id, resource_group):
    '''Get details about the application security groups for a resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.

    Returns:
        HTTP response. ASG JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/virtualNetworks/',
                        '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_asgs_all(access_token, subscription_id):
    '''Get details about the application security groups for a resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. ASG JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Network/virtualNetworks/',
                        '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_lb_nat_rules(access_token, subscription_id, resource_group, lb_name):
    '''List the inbound NAT rules for a load balancer.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        lb_name (str): Name of the load balancer.

    Returns:
        HTTP response. JSON body of load balancer NAT rules.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/loadBalancers/', lb_name,
                        'inboundNatRules?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_load_balancers(access_token, subscription_id):
    '''List the load balancers in a subscription.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. JSON body of load balancer list with properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Network/',
                        '/loadBalancers?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_load_balancers_rg(access_token, subscription_id, resource_group):
    '''List the load balancers in a resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.

    Returns:
        HTTP response. JSON body of load balancer list with properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/',
                        '/loadBalancers?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_nics(access_token, subscription_id):
    '''List the network interfaces in a subscription.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. JSON body of NICs list with properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Network/',
                        '/networkInterfaces?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_nics_rg(access_token, subscription_id, resource_group):
    '''List network interface cards within a resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.

    Returns:
        HTTP response. JSON body of load balancer list with properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/',
                        '/networkInterfaces?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_nsgs(access_token, subscription_id, resource_group):
    ''' List all network security security groups in a resource group.

    Args:
        access_token (str): a valid Azure Authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name
    Returns:
        HTTP response. JSON body of network security groups list with properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                '/subscriptions/', subscription_id,
                '/resourceGroups/', resource_group,
                '/providers/Microsoft.Network/',
                '/networkSecurityGroups?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_nsgs_all(access_token, subscription_id):
    '''List all network security groups in a subscription.
    Args:
        access_token (str): a valid Azure Authentication token.
        subscription_id (str): Azure subscription id.
    Returns:
            HTTP response. JSON body of all network security groups in a subscription.

    '''
    endpoint = ''.join([get_rm_endpoint(),
                '/subscriptions/', subscription_id,
                '/providers/Microsoft.Network/',
                'networkSEcurityGroups?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_public_ips(access_token, subscription_id, resource_group):
    '''List the public ip addresses in a resource group	.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.

    Returns:
        HTTP response. JSON body of public IPs list with properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/',
                        'publicIPAddresses?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_vnets(access_token, subscription_id):
    '''List the VNETs in a subscription	.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. JSON body of VNets list with properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Network/',
                        '/virtualNetworks?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_vnets_rg(access_token, subscription_id, resource_group):
    '''List the VNETs in a resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.

    Returns:
        HTTP response. JSON body of VNets list with properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/',
                        '/virtualNetworks?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def update_load_balancer(access_token, subscription_id, resource_group, lb_name, body):
    '''Updates a load balancer model, i.e. PUT an updated LB body.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        lb_name (str): Name of the new load balancer.
        body (str): JSON body of an updated load balancer.

    Returns:
        HTTP response. Load Balancer JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Network/loadBalancers/', lb_name,
                        '?api-version=', NETWORK_API])
    return do_put(endpoint, body, access_token)
