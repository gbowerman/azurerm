'''computerp.py - azurerm functions for the Microsoft.Compute resource provider'''

import json

from .restfns import do_delete, do_get, do_get_next, do_patch, do_post, do_put
from .settings import COMP_API, NETWORK_API, get_rm_endpoint


def create_as(access_token, subscription_id, resource_group, as_name,
              update_domains, fault_domains, location):
    '''Create availability set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        as_name (str): Name of the new availability set.
        update_domains (int): Number of update domains.
        fault_domains (int): Number of fault domains.
        location (str): Azure data center location. E.g. westus.

    Returns:
        HTTP response. JSON body of the availability set properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/availabilitySets/', as_name,
                        '?api-version=', COMP_API])
    as_body = {'location': location}
    properties = {'platformUpdateDomainCount': update_domains}
    properties['platformFaultDomainCount'] = fault_domains
    as_body['properties'] = properties
    body = json.dumps(as_body)
    return do_put(endpoint, body, access_token)


def create_vm(access_token, subscription_id, resource_group, vm_name, vm_size, publisher, offer,
              sku, version, nic_id, location, storage_type='Standard_LRS', osdisk_name=None,
              username='azure', password=None, public_key=None):
    '''Create a new Azure virtual machine.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vm_name (str): Name of the new virtual machine.
        vm_size (str): Size of virtual machine, e.g. 'Standard_D1_v2'.
        publisher (str): VM image publisher. E.g. 'MicrosoftWindowsServer'.
        offer (str): VM image offer. E.g. 'WindowsServer'.
        sku (str): VM image sku. E.g. '2016-Datacenter'.
        version (str): VM image version. E.g. 'latest'.
        nic_id (str): Resource id of a NIC.
        location (str): Azure data center location. E.g. westus.
        storage_type (str): Optional storage type. Default 'Standard_LRS'.
        osdisk_name (str): Optional OS disk name. Default is None.
        username (str): Optional user name. Default is 'azure'.
        password (str): Optional password. Default is None (not required if using public_key).
        public_key (str): Optional public key. Default is None (not required if using password,
            e.g. on Windows).

    Returns:
        HTTP response. JSON body of the virtual machine properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '?api-version=', COMP_API])
    if osdisk_name is None:
        osdisk_name = vm_name + 'osdisk'
    vm_body = {'name': vm_name}
    vm_body['location'] = location
    properties = {'hardwareProfile': {'vmSize': vm_size}}
    image_reference = {'publisher': publisher,
                       'offer': offer, 'sku': sku, 'version': version}
    storage_profile = {'imageReference': image_reference}
    os_disk = {'name': osdisk_name}
    os_disk['managedDisk'] = {'storageAccountType': storage_type}
    os_disk['caching'] = 'ReadWrite'
    os_disk['createOption'] = 'fromImage'
    storage_profile['osDisk'] = os_disk
    properties['storageProfile'] = storage_profile
    os_profile = {'computerName': vm_name}
    os_profile['adminUsername'] = username
    if password is not None:
        os_profile['adminPassword'] = password
    if public_key is not None:
        if password is None:
            disable_pswd = True
        else:
            disable_pswd = False
        linux_config = {'disablePasswordAuthentication': disable_pswd}
        pub_key = {'path': '/home/' + username + '/.ssh/authorized_keys'}
        pub_key['keyData'] = public_key
        linux_config['ssh'] = {'publicKeys': [pub_key]}
        os_profile['linuxConfiguration'] = linux_config
    properties['osProfile'] = os_profile
    network_profile = {'networkInterfaces': [
        {'id': nic_id, 'properties': {'primary': True}}]}
    properties['networkProfile'] = network_profile
    vm_body['properties'] = properties
    body = json.dumps(vm_body)
    return do_put(endpoint, body, access_token)


def create_vmss(access_token, subscription_id, resource_group, vmss_name, vm_size, capacity,
                publisher, offer, sku, version, subnet_id, be_pool_id, lb_pool_id, location,
                storage_type='Standard_LRS', username='azure', password=None, public_key=None,
                overprovision=True, upgrade_policy='Manual', public_ip_per_vm=False):
    '''Create virtual machine scale set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the new scale set.
        vm_size (str): Size of virtual machine, e.g. 'Standard_D1_v2'.
        capacity (int): Number of VMs in the scale set. 0-1000.
        publisher (str): VM image publisher. E.g. 'MicrosoftWindowsServer'.
        offer (str): VM image offer. E.g. 'WindowsServer'.
        sku (str): VM image sku. E.g. '2016-Datacenter'.
        version (str): VM image version. E.g. 'latest'.
        subnet_id (str): Resource id of a subnet.
        be_pool_id (str): Resource id of a backend NAT pool.
        lb_pool_id (str): Resource id of a load balancer pool.
        location (str): Azure data center location. E.g. westus.
        storage_type (str): Optional storage type. Default 'Standard_LRS'.
        username (str): Optional user name. Default is 'azure'.
        password (str): Optional password. Default is None (not required if using public_key).
        public_key (str): Optional public key. Default is None (not required if using password,
            e.g. on Windows).
        overprovision (bool): Optional. Enable overprovisioning of VMs. Default True.
        upgrade_policy (str): Optional. Set upgrade policy to Automatic, Manual or Rolling.
            Default 'Manual'.
        public_ip_per_vm (bool): Optional. Set public IP per VM. Default False.

    To do:
        Make the LB pool arguments optional.

    Returns:
        HTTP response. JSON body of the virtual machine scale set properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '?api-version=', COMP_API])

    vmss_body = {'location': location}
    vmss_sku = {'name': vm_size, 'tier': 'Standard', 'capacity': capacity}
    vmss_body['sku'] = vmss_sku
    properties = {'overprovision': overprovision}
    properties['upgradePolicy'] = {'mode': upgrade_policy}
    os_profile = {'computerNamePrefix': vmss_name}
    os_profile['adminUsername'] = username
    if password is not None:
        os_profile['adminPassword'] = password
    if public_key is not None:
        if password is None:
            disable_pswd = True
        else:
            disable_pswd = False
        linux_config = {'disablePasswordAuthentication': disable_pswd}
        pub_key = {'path': '/home/' + username + '/.ssh/authorized_keys'}
        pub_key['keyData'] = public_key
        linux_config['ssh'] = {'publicKeys': [pub_key]}
        os_profile['linuxConfiguration'] = linux_config
    vm_profile = {'osProfile': os_profile}
    os_disk = {'createOption': 'fromImage'}
    os_disk['managedDisk'] = {'storageAccountType': storage_type}
    os_disk['caching'] = 'ReadWrite'
    storage_profile = {'osDisk': os_disk}
    storage_profile['imageReference'] = \
        {'publisher': publisher, 'offer': offer, 'sku': sku, 'version': version}
    vm_profile['storageProfile'] = storage_profile
    nic = {'name': vmss_name}
    ip_config = {'name': vmss_name}
    ip_properties = {'subnet': {'id': subnet_id}}
    ip_properties['loadBalancerBackendAddressPools'] = [{'id': be_pool_id}]
    ip_properties['loadBalancerInboundNatPools'] = [{'id': lb_pool_id}]
    if public_ip_per_vm is True:
        ip_properties['publicIpAddressConfiguration'] = {
            'name': 'pubip', 'properties': {'idleTimeoutInMinutes': 15}}
    ip_config['properties'] = ip_properties
    nic['properties'] = {'primary': True, 'ipConfigurations': [ip_config]}
    network_profile = {'networkInterfaceConfigurations': [nic]}
    vm_profile['networkProfile'] = network_profile
    properties['virtualMachineProfile'] = vm_profile
    vmss_body['properties'] = properties

    body = json.dumps(vmss_body)
    return do_put(endpoint, body, access_token)


def deallocate_vm(access_token, subscription_id, resource_group, vm_name):
    '''Stop-deallocate a virtual machine.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vm_name (str): Name of the virtual machine.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '/deallocate',
                        '?api-version=', COMP_API])
    return do_post(endpoint, '', access_token)


def delete_as(access_token, subscription_id, resource_group, as_name):
    '''Delete availability set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        as_name (str): Name of the availability set.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/availabilitySets/', as_name,
                        '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)


def delete_vm(access_token, subscription_id, resource_group, vm_name):
    '''Delete a virtual machine.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vm_name (str): Name of the virtual machine.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)


def delete_vmss(access_token, subscription_id, resource_group, vmss_name):
    '''Delete a virtual machine scale set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)


def delete_vmss_vms(access_token, subscription_id, resource_group, vmss_name, vm_ids):
    '''Delete a VM in a VM Scale Set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.
        vm_ids (str): String representation of a JSON list of VM IDs. E.g. '[1,2]'.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/delete?api-version=', COMP_API])
    body = '{"instanceIds" : ' + vm_ids + '}'
    return do_post(endpoint, body, access_token)


def get_compute_usage(access_token, subscription_id, location):
    '''List compute usage and limits for a location.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        location (str): Azure data center location. E.g. westus.

    Returns:
        HTTP response. JSON body of Compute usage and limits data.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.compute/locations/', location,
                        '/usages?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vm(access_token, subscription_id, resource_group, vm_name):
    '''Get virtual machine details.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vm_name (str): Name of the virtual machine.

    Returns:
        HTTP response. JSON body of VM properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vm_extension(access_token, subscription_id, resource_group, vm_name, extension_name):
    '''Get details about a VM extension.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vm_name (str): Name of the virtual machine.
        extension_name (str): VM extension name.

    Returns:
        HTTP response. JSON body of VM extension properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '/extensions/', extension_name,
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vm_instance_view(access_token, subscription_id, resource_group, vm_name):
    '''Get operational details about the state of a VM.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vm_name (str): Name of the virtual machine.

    Returns:
        HTTP response. JSON body of VM instance view details.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '/InstanceView?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss(access_token, subscription_id, resource_group, vmss_name):
    '''Get virtual machine scale set details.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.

    Returns:
        HTTP response. JSON body of scale set properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_instance_view(access_token, subscription_id, resource_group, vmss_name):
    '''Get virtual machine scale set instance view.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.

    Returns:
        HTTP response. JSON body of VM instance view details.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/instanceView?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_nics(access_token, subscription_id, resource_group, vmss_name):
    '''Get NIC details for a VM Scale Set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.

    Returns:
        HTTP response. JSON body of VMSS NICs.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/networkInterfaces?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_public_ips(access_token, subscription_id, resource_group, vmss_name):
    '''Get public IP address details for a VM scale set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.

    Returns:
        HTTP response. JSON body of list of public IPs.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/publicipaddresses?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_rolling_upgrades(access_token, subscription_id, resource_group, vmss_name):
    '''Get details of the latest VM scale set rolling upgrade.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.

    Returns:
        HTTP response. JSON body of rolling upgrades status.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/rollingUpgrades/latest?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_vm(access_token, subscription_id, resource_group, vmss_name, instance_id):
    '''Get individual VMSS VM details.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.
        instance_id (int): VM ID of the scale set VM.

    Returns:
        HTTP response. JSON body of VMSS VM model view.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/virtualMachines/', str(instance_id),
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name,
                              instance_id):
    '''Get individual VMSS VM instance view.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.
        instance_id (int): VM ID of the scale set VM.

    Returns:
        HTTP response. JSON body of VMSS VM instance view.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/virtualMachines/', str(instance_id),
                        '/instanceView?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_vm_nics(access_token, subscription_id, resource_group, vmss_name, instance_id):
    '''Get NIC details for a VMSS VM.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.
        instance_id (int): VM ID of the scale set VM.

    Returns:
        HTTP response. JSON body of VMSS VM instance view.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/virtualMachines/', str(instance_id),
                        '/networkInterfaces?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def get_as(access_token, subscription_id, resource_group, as_name):
    '''Get availability set details.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        as_name (str): Name of the new availability set.

    Returns:
        HTTP response. JSON body of the availability set properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/availabilitySets/', as_name,
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_as(access_token, subscription_id, resource_group):
    '''List availability sets in a resource_group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.

    Returns:
        HTTP response. JSON body of the list of availability set properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/availabilitySets',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_as_sub(access_token, subscription_id):
    '''List availability sets in a subscription.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. JSON body of the list of availability set properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/availabilitySets',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vm_images_sub(access_token, subscription_id):
    '''List VM images in a subscription.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. JSON body of a list of VM images.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/images',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vm_instance_view(access_token, subscription_id, resource_group):
    '''List VM instances views in a resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.

    Returns:
        HTTP response. JSON body of a list of VM instance views.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines',
                        '?$expand=instanceView&$select=instanceView&api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vms(access_token, subscription_id, resource_group):
    '''List VMs in a resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.

    Returns:
        HTTP response. JSON body of a list of VM model views.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines',
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_vms_sub(access_token, subscription_id):
    '''List VMs in a subscription.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. JSON body of a list of VM model views.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/virtualMachines',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vmss(access_token, subscription_id, resource_group):
    '''List VM Scale Sets in a resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.

    Returns:
        HTTP response. JSON body of a list of scale set model views.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vmss_skus(access_token, subscription_id, resource_group, vmss_name):
    '''List the VM skus available for a VM Scale Set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.

    Returns:
        HTTP response. JSON body of VM skus.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/skus',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vmss_sub(access_token, subscription_id):
    '''List VM Scale Sets in a subscription.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. JSON body of VM scale sets.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name):
    '''List the instance views for all the VMs in a VM scale set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.

    Returns:
        HTTP response. JSON body of list of VM instance views.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/virtualMachines?$expand=instanceView&$select=instanceView&api-version=',
                        COMP_API])
    return do_get_next(endpoint, access_token)


def list_vmss_vm_instance_view_pg(access_token, subscription_id, resource_group, vmss_name,
                                  link=None):
    '''Gets one page of a paginated list of scale set VM instance views.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.
        link (str): Optional link to URI to get list (as part of a paginated API query).

    Returns:
        HTTP response. JSON body of list of VM instance views.
    '''
    if link is None:
        endpoint = ''.join([get_rm_endpoint(),
                            '/subscriptions/', subscription_id,
                            '/resourceGroups/', resource_group,
                            '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                            '/virtualMachines?$expand=instanceView&$select=instanceView',
                            '&api-version=', COMP_API])
    else:
        endpoint = link
    return do_get(endpoint, access_token)


def list_vmss_vms(access_token, subscription_id, resource_group, vmss_name):
    '''List the VMs in a VM Scale Set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.

    Returns:
        HTTP response. JSON body of list of VM model views.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/virtualMachines',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def poweroff_vmss(access_token, subscription_id, resource_group, vmss_name):
    '''Power off all the VMs in a virtual machine scale set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/powerOff?api-version=', COMP_API])
    body = '{"instanceIds" : ["*"]}'
    return do_post(endpoint, body, access_token)


def poweroff_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    '''Poweroff all the VMs in a virtual machine scale set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.
        instance_ids (str): String representation of a JSON list of VM IDs. E.g. '[1,2]'.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/powerOff?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


def reimage_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    '''Drive is reset, temp drive is not).

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.
        instance_ids (str): String representation of a JSON list of VM IDs. E.g. '[1,2]'.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/reimage?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


def restart_vm(access_token, subscription_id, resource_group, vm_name):
    '''Restart a virtual machine.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vm_name (str): Name of the virtual machine.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/',
                        vm_name,
                        '/restart',
                        '?api-version=', COMP_API])
    return do_post(endpoint, '', access_token)


def restart_vmss(access_token, subscription_id, resource_group, vmss_name):
    '''Restart all the VMs in a virtual machine scale set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/restart?api-version=', COMP_API])
    body = '{"instanceIds" : ["*"]}'
    return do_post(endpoint, body, access_token)


def restart_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    '''Restart a specific VM in a virtual machine scale set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.
        instance_ids (str): String representation of a JSON list of VM IDs. E.g. '[1,2]'.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/restart?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


def scale_vmss(access_token, subscription_id, resource_group, vmss_name, size, tier, capacity):
    '''Change the instance count of an existing VM Scale Set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.
        size (str): VM size. E.g. 'Standard_D1_v2'.
        tier (str): VM tier. E.g. 'Standard'.
        capacity (int): New number of VMs.
    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '?api-version=', COMP_API])
    body = '{"sku":{ "name":"' + size + '", "tier":"' + \
        tier + '", "capacity":"' + str(capacity) + '"}}'
    return do_patch(endpoint, body, access_token)


def start_vm(access_token, subscription_id, resource_group, vm_name):
    '''Start a virtual machine.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vm_name (str): Name of the virtual machine.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/',
                        vm_name,
                        '/start',
                        '?api-version=', COMP_API])
    return do_post(endpoint, '', access_token)


def start_vmss(access_token, subscription_id, resource_group, vmss_name):
    '''Start all the VMs in a virtual machine scale set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/start?api-version=', COMP_API])
    body = '{"instanceIds" : ["*"]}'
    return do_post(endpoint, body, access_token)


def start_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    '''Start all the VMs in a virtual machine scale set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.
        instance_ids (str): String representation of a JSON list of VM IDs. E.g. '[1,2]'.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/start?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


def stopdealloc_vmss(access_token, subscription_id, resource_group, vmss_name):
    '''Stop all the VMs in a virtual machine scale set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/deallocate?api-version=', COMP_API])
    body = '{"instanceIds" : ["*"]}'
    return do_post(endpoint, body, access_token)


def stopdealloc_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    '''Stop the specified VMs in a virtual machine scale set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.
        instance_ids (str): String representation of a JSON list of VM IDs. E.g. '[1,2]'.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/deallocate?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


def stop_vm(access_token, subscription_id, resource_group, vm_name):
    '''Stop a virtual machine but don't deallocate resources (power off).

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vm_name (str): Name of the virtual machine.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/',
                        vm_name,
                        '/powerOff',
                        '?api-version=', COMP_API])
    return do_post(endpoint, '', access_token)


def update_vm(access_token, subscription_id, resource_group, vm_name, body):
    '''Update a virtual machine with a new JSON body. E.g. do a GET, change something, call this.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vm_name (str): Name of the virtual machine.
        body (dict): JSON body of the VM.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '?api-version=', COMP_API])
    return do_put(endpoint, body, access_token)


def update_vmss(access_token, subscription_id, resource_group, vmss_name, body):
    '''Update a VMSS with a new JSON body. E.g. do a GET, change something, call this.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vm_name (str): Name of the virtual machine.
        body (dict): JSON body of the VM scale set.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '?api-version=', COMP_API])
    return do_put(endpoint, body, access_token)


def upgrade_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    '''Upgrade specific VMs in a virtual machine scale set.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        vmss_name (str): Name of the virtual machine scale set.
        instance_ids (str): String representation of a JSON list of VM IDs. E.g. '[1,2]'.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/manualupgrade?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)
