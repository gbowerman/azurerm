'''computerp.py - azurerm functions for the Microsoft.Compute resource provider'''

from .restfns import do_delete, do_get, do_get_next, do_patch, do_post, do_put
from .settings import get_rm_endpoint, COMP_API, NETWORK_API
import json


# create_as(access_token, subscription_id, resource_group, as_name, \
def create_as(access_token, subscription_id, resource_group, as_name,
              update_domains, fault_domains, location):
    '''Create availability set.
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


# create_vm(access_token, subscription_id, resource_group, vm_name, vm_size, publisher, offer,
#         sku, version, nic_id, location, storage_type='standard_LRS', username='azure',
#         password=None, public_key=None)
def create_vm(access_token, subscription_id, resource_group, vm_name, vm_size, publisher, offer,
              sku, version, nic_id, location, storage_type='Standard_LRS', osdisk_name=None,
              username='azure', password=None, public_key=None):
    '''Template might be easier.
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


# create_vmss(access_token, subscription_id, resource_group, vmss_name, vm_size, capacity, \
#   publisher, offer, sku, version, subnet_id, be_pool_id, lb_pool_id, \
#   location, storage_type='Standard_LRS', username='azure', password=None, public_key=None, overprovision='true', \
def create_vmss(access_token, subscription_id, resource_group, vmss_name, vm_size, capacity,
                publisher, offer, sku, version, subnet_id, be_pool_id, lb_pool_id, location, storage_type='Standard_LRS',
                username='azure', password=None, public_key=None, overprovision='true',
                upgradePolicy='Manual', public_ip_per_vm=False):
    '''Create virtual machine scale set.
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
    properties['upgradePolicy'] = {'mode': upgradePolicy}
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
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/availabilitySets/', as_name,
                        '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)


def delete_vm(access_token, subscription_id, resource_group, vm_name):
    '''Delete a virtual machine.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)


def delete_vmss(access_token, subscription_id, resource_group, vmss_name):
    '''Delete a virtual machine scale set.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)


def delete_vmss_vms(access_token, subscription_id, resource_group, vmss_name, vm_ids):
    '''Delete a VM in a VM Scale Set.
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
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.compute/locations/', location,
                        '/usages?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vm(access_token, subscription_id, resource_group, vm_name):
    '''Get virtual machine details.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vm_extension(access_token, subscription_id, resource_group, vm_name, extension_name):
    '''Get details about a VM extension.
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
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '/InstanceView?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss(access_token, subscription_id, resource_group, vmss_name):
    '''Get virtual machine scale set details.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_instance_view(access_token, subscription_id, resource_group, vmss_name):
    '''Get virtual machine scale set instance view.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/instanceView?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_nics(access_token, subscription_id, resource_group, vmss_name):
    '''Get NIC details for a VM Scale Set.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/networkInterfaces?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_public_ips(access_token, subscription_id, resource_group, vmss_name):
    '''Get public IP address details for a VM scale set.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/publicipaddresses?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_rolling_upgrades(access_token, subscription_id, resource_group, vmss_name):
    '''Get details of the latest VM scale set rolling upgrade.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/rollingUpgrades/latest?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_vm(access_token, subscription_id, resource_group, vmss_name, instance_id):
    '''Get individual VMSS VM details.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/virtualMachines/', str(instance_id),
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name, instance_id):
    '''Get individual VMSS VM instance view.
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
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/virtualMachines/', str(instance_id),
                        '/networkInterfaces?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def get_as(access_token, subscription_id, resource_group, as_name):
    '''Get availability set.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/availabilitySets/', as_name,
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_as(access_token, subscription_id, resource_group):
    '''List availability sets in a resource_group.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/availabilitySets',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_as_sub(access_token, subscription_id):
    '''List availability sets in a subscription.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/availabilitySets',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vm_images_sub(access_token, subscription_id):
    '''List VM images in a subscription.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/images',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vm_instance_view(access_token, subscription_id, resource_group):
    '''List VM instances views in a resource group.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines',
                        '?$expand=instanceView&$select=instanceView&api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vms(access_token, subscription_id, resource_group):
    '''List VMs in a resource group.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines',
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_vms_sub(access_token, subscription_id):
    '''List VMs in a subscription.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/virtualMachines',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vmss(access_token, subscription_id, resource_group):
    '''List VM Scale Sets in a resource group.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vmss_skus(access_token, subscription_id, resource_group, vmss_name):
    '''List the VM skus available for a VM Scale Set.
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
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


# list_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name)
def list_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name):
    '''All of them in a loop.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/virtualMachines?$expand=instanceView&$select=instanceView&api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vmss_vm_instance_view_pg(access_token, subscription_id, resource_group, vmss_name, link=None):
    '''Gets one page of a paginated list of scale set VM instance views.
    '''
    if link is None:
        endpoint = ''.join([get_rm_endpoint(),
                            '/subscriptions/', subscription_id,
                            '/resourceGroups/', resource_group,
                            '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                            '/virtualMachines?$expand=instanceView&$select=instanceView&api-version=', COMP_API])
    else:
        endpoint = link
    return do_get(endpoint, access_token)


def list_vmss_vms(access_token, subscription_id, resource_group, vmss_name):
    '''List the VMs in a VM Scale Set.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/virtualMachines',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def poweroff_vmss(access_token, subscription_id, resource_group, vmss_name):
    '''Poweroff all the VMs in a virtual machine scale set.
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
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/powerOff?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


# reimage_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids)
def reimage_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    '''Drive is reset, temp drive is not).
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
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '?api-version=', COMP_API])
    body = '{"sku":{ "name":"' + size + '", "tier":"' + \
        tier + '", "capacity":"' + str(capacity) + '"}}'
    return do_patch(endpoint, body, access_token)


# scale_vmss_lite(access_token, subscription_id, resource_group, vmss_name, size, tier, capacity)
def scale_vmss_lite(access_token, subscription_id, resource_group, vmss_name, capacity):
    '''Capacity only.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '?api-version=', COMP_API])
    body = '{"sku":{"capacity":"' + str(capacity) + '"}}'
    return do_patch(endpoint, body, access_token)


def start_vm(access_token, subscription_id, resource_group, vm_name):
    '''Start a virtual machine.
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
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/deallocate?api-version=', COMP_API])
    body = '{"instanceIds" : ["*"]}'
    return do_post(endpoint, body, access_token)


def stopdealloc_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    '''Stop all the VMs in a virtual machine scale set.
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
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/',
                        vm_name,
                        '/powerOff',
                        '?api-version=', COMP_API])
    return do_post(endpoint, '', access_token)


# update_vm(access_token, subscription_id, resource_group, vm_name, body)
def update_vm(access_token, subscription_id, resource_group, vm_name, body):
    '''Sku version.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '?api-version=', COMP_API])
    return do_put(endpoint, body, access_token)


# update_vmss(access_token, subscription_id, resource_group, vmss_name, body)
def update_vmss(access_token, subscription_id, resource_group, vmss_name, body):
    '''Body, e.g. a sku version.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '?api-version=', COMP_API])
    return do_put(endpoint, body, access_token)


def upgrade_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    '''Upgrade specific VMs in a virtual machine scale set.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/manualupgrade?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)
