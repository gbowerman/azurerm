# computerp.py - azurerm functions for the Microsoft.Compute resource provider

from .restfns import do_delete, do_get, do_get_next, do_patch, do_post, do_put
from .settings import azure_rm_endpoint, COMP_API, NETWORK_API
import json


# create_as(access_token, subscription_id, resource_group, as_name, \
#   update_domains, fault_domains, location)
# create availability set
def create_as(access_token, subscription_id, resource_group, as_name,
              update_domains, fault_domains, location):

    endpoint = ''.join([azure_rm_endpoint,
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


# create_vm(access_token, subscription_id, resource_group, vm_name, vm_size, publisher, offer, sku, version,
#              nic_id, location, storage_type='standard_LRS', username='azure', password=None, public_key=None)
# create a simple virtual machine - in most cases deploying an ARM template might be easier
def create_vm(access_token, subscription_id, resource_group, vm_name, vm_size, publisher, offer, sku, version,
              nic_id, location, storage_type='Standard_LRS', username='azure', password=None, public_key=None):
    endpoint = ''.join([azure_rm_endpoint,
                '/subscriptions/', subscription_id,
                '/resourceGroups/', resource_group,
                '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                '?api-version=', COMP_API])
    vm_body = {'name': vm_name}
    vm_body['location'] = location
    properties = {'hardwareProfile': {'vmSize': vm_size}}
    image_reference = {'publisher': publisher, 'offer': offer, 'sku': sku, 'version': version}
    storage_profile = {'imageReference': image_reference}
    os_disk = {'name': 'osdisk1'}
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
        pub_key = {'path': '/home/' + username +'/.ssh/authorized_keys'}
        pub_key['keyData'] = public_key
        linux_config['ssh'] = {'publicKeys': [pub_key]}
        os_profile['linuxConfiguration'] = linux_config
    properties['osProfile'] = os_profile
    network_profile = {'networkInterfaces': [{'id': nic_id, 'properties': {'primary': True}}]}
    properties['networkProfile'] = network_profile
    vm_body['properties'] = properties
    body = json.dumps(vm_body)
    return do_put(endpoint, body, access_token)


# create_vmss(access_token, subscription_id, resource_group, vmss_name, vm_size, capacity, \
#   publisher, offer, sku, version, subnet_id, be_pool_id, lb_pool_id, \
#   location, storage_type='Standard_LRS', username='azure', password=None, public_key=None, overprovision='true', \
#   upgradePolicy='Manual')
# create virtual machine scale set
def create_vmss(access_token, subscription_id, resource_group, vmss_name, vm_size, capacity, \
    publisher, offer, sku, version, subnet_id, be_pool_id, lb_pool_id, location, storage_type='Standard_LRS', \
     username='azure', password=None, public_key=None, overprovision='true', \
    upgradePolicy='Manual'):
    endpoint = ''.join([azure_rm_endpoint,
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
        pub_key = {'path': '/home/' + username +'/.ssh/authorized_keys'}
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
    ip_properties = {'subnet': { 'id': subnet_id}}
    ip_properties['loadBalancerBackendAddressPools'] = [{'id': be_pool_id}]
    ip_properties['loadBalancerInboundNatPools'] = [{'id': lb_pool_id}]
    ip_config['properties'] = ip_properties
    nic['properties'] = {'primary': True, 'ipConfigurations': [ip_config]}
    network_profile = {'networkInterfaceConfigurations': [nic]}
    vm_profile['networkProfile'] = network_profile
    properties['virtualMachineProfile'] = vm_profile
    vmss_body['properties'] = properties

    body = json.dumps(vmss_body)
    return do_put(endpoint, body, access_token)


# deallocate_vm(access_token, subscription_id, resource_group, vm_name)
# stop-deallocate a virtual machine
def deallocate_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '/deallocate',
                        '?api-version=', COMP_API])
    return do_post(endpoint, '', access_token)


# delete_as(access_token, subscription_id, resource_group, as_name)
# delete availability set
def delete_as(access_token, subscription_id, resource_group, as_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/availabilitySets/', as_name,
                        '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)


# delete_vm(access_token, subscription_id, resource_group, vm_name)
# delete a virtual machine
def delete_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)


# delete_vmss(access_token, subscription_id, resource_group, vmss_name)
# delete a virtual machine scale set
def delete_vmss(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)


# delete_vmss_vm(access_token, subscription_id, resource_group, vmss_name, vm_ids)
# delete a VM in a VM Scale Set
def delete_vmss_vms(access_token, subscription_id, resource_group, vmss_name, vm_ids):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/delete?api-version=', COMP_API])
    body = '{"instanceIds" : ' + vm_ids + '}'
    return do_post(endpoint, body, access_token)


# get_compute_usage(access_token, subscription_id, location)
# list compute usage and limits for a location
def get_compute_usage(access_token, subscription_id, location):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.compute/locations/', location,
                        '/usages?api-version=', COMP_API])
    return do_get(endpoint, access_token)


# get_vm(access_token, subscription_id, resource_group, vm_name)
# get virtual machine details
def get_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


# get_vm_extension(access_token, subscription_id, resource_group, vm_name, extension_name)
# get details about a VM extension
def get_vm_extension(access_token, subscription_id, resource_group, vm_name, extension_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '/extensions/', extension_name,
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


# get_vm_instance(access_token, subscription_id, resource_group, vm_name)
# get operational details about the state of a VM
def get_vm_instance_view(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '/InstanceView?api-version=', COMP_API])
    return do_get(endpoint, access_token)


# get_vmss(access_token, subscription_id, resource_group, vmss_name)
# get virtual machine scale set details
def get_vmss(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


# get_vmss_instance_view(access_token, subscription_id, resource_group, vmss_name)
# get virtual machine scale set instance view
def get_vmss_instance_view(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/instanceView?api-version=', COMP_API])
    return do_get(endpoint, access_token)


# get_vmss_nics(access_token, subscription_id, resource_group, vmss_name)
# get NIC details for a VM Scale Set
def get_vmss_nics(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/networkInterfaces?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


# get_vmss_vm(access_token, subscription_id, resource_group, vmss_name, instance_id)
# get individual VMSS VM details
def get_vmss_vm(access_token, subscription_id, resource_group, vmss_name, instance_id):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/virtualMachines/', str(instance_id),
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


# get_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name, instance_id)
# get individual VMSS VM instance view
def get_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name, instance_id):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/virtualMachines/', str(instance_id),
                        '/instanceView?api-version=', COMP_API])
    return do_get(endpoint, access_token)


# get_vmss_vm_nics(access_token, subscription_id, resource_group, vmss_name, instance_id)
# get NIC details for a VMSS VM
def get_vmss_vm_nics(access_token, subscription_id, resource_group, vmss_name, instance_id):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/virtualMachines/', str(instance_id),
                        '/networkInterfaces?api-version=', COMP_API])
    return do_get(endpoint, access_token)


# get_as(access_token, subscription_id, resource_group, as_name)
# get availability set
def get_as(access_token, subscription_id, resource_group, as_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/availabilitySets/', as_name,
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


# list_as_sub(access_token, subscription_id, resource_group)
# list availability sets in a resource_group
def list_as(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/availabilitySets',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


# list_as_sub(access_token, subscription_id)
# list availability sets in a subscription
def list_as_sub(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/availabilitySets',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)



# list_vm_images_sub(access_token, subscription_id)
# list VM images in a subscription
def list_vm_images_sub(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/images',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


# list_vm_instance_view(access_token, subscription_id, resource_group)
# list VM instances views in a resource group
def list_vm_instance_view(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines',
                        '?$expand=instanceView&$select=instanceView&api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


# list_vms(access_token, subscription_id, resource_group)
# list VMs in a resource group
def list_vms(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines',
                        '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


# list_vms_sub(access_token, subscription_id)
# list VMs in a subscription
def list_vms_sub(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/virtualMachines',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


# list_vmss(access_token, subscription_id, resource_group)
# list VM Scale Sets in a resource group
def list_vmss(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


# list_vmss_skus(access_token, subscription_id, resource_group, vmss_name)
# list the VM skus available for a VM Scale Set
def list_vmss_skus(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/skus',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


# list_vmss_sub(access_token, subscription_id)
# list VM Scale Sets in a subscription
def list_vmss_sub(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


# list_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name)
# list the VMSS VM instance views in a scale set - uses do_get_next to get all of them in a loop
def list_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/virtualMachines?$expand=instanceView&$select=instanceView&api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


# list_vmss_vm_instance_view_pg(access_token, subscription_id, resource_group, vmss_name)
# gets one page of a paginated list of scale set VM instance views
def list_vmss_vm_instance_view_pg(access_token, subscription_id, resource_group, vmss_name, link=None):
    if link is None:
        endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/virtualMachines?$expand=instanceView&$select=instanceView&api-version=', COMP_API])
    else:
        endpoint = link
    return do_get(endpoint, access_token)


# list_vmss_vms(access_token, subscription_id, resource_group, vmss_name)
# list the VMs in a VM Scale Set
def list_vmss_vms(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/virtualMachines',
                        '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


# poweroff_vmss(access_token, subscription_id, resource_group, vmss_name)
# poweroff all the VMs in a virtual machine scale set
def poweroff_vmss(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/powerOff?api-version=', COMP_API])
    body = '{"instanceIds" : ["*"]}'
    return do_post(endpoint, body, access_token)


# poweroff_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids)
# poweroff all the VMs in a virtual machine scale set
def poweroff_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/powerOff?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


# reimage_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids)
# reset specific VMs a virtual machine scale set to factory settings (OS drive is reset, temp drive is not)
def reimage_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/reimage?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


# restart_vm(access_token, subscription_id, resource_group, vm_name)
# restart a virtual machine
def restart_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/',
                        vm_name,
                        '/restart',
                        '?api-version=', COMP_API])
    return do_post(endpoint, '', access_token)


# restart_vmss(access_token, subscription_id, resource_group, vmss_name)
# restart all the VMs in a virtual machine scale set
def restart_vmss(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/restart?api-version=', COMP_API])
    body = '{"instanceIds" : ["*"]}'
    return do_post(endpoint, body, access_token)


# restart_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids)
# restart a specific VM in a virtual machine scale set
def restart_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/restart?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


# scale_vmss(access_token, subscription_id, resource_group, vmss_name, size, tier, capacity)
# change the instance count of an existing VM Scale Set
def scale_vmss(access_token, subscription_id, resource_group, vmss_name, size, tier, capacity):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '?api-version=', COMP_API])
    body = '{"sku":{ "name":"' + size + '", "tier":"' + tier + '", "capacity":"' + str(capacity) + '"}}'
    return do_patch(endpoint, body, access_token)


# start_vm(access_token, subscription_id, resource_group, vm_name)
# start a virtual machine
def start_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/',
                        vm_name,
                        '/start',
                        '?api-version=', COMP_API])
    return do_post(endpoint, '', access_token)


# start_vmss(access_token, subscription_id, resource_group, vmss_name)
# start all the VMs in a virtual machine scale set
def start_vmss(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/start?api-version=', COMP_API])
    body = '{"instanceIds" : ["*"]}'
    return do_post(endpoint, body, access_token)


# start_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids)
# start all the VMs in a virtual machine scale set
def start_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/start?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


# stopdalloc_vmss(access_token, subscription_id, resource_group, vmss_name)
# stop all the VMs in a virtual machine scale set
def stopdealloc_vmss(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/deallocate?api-version=', COMP_API])
    body = '{"instanceIds" : ["*"]}'
    return do_post(endpoint, body, access_token)


# stopdealloc_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids)
# stop all the VMs in a virtual machine scale set
def stopdealloc_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/deallocate?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


# stop_vm(access_token, subscription_id, resource_group, vm_name)
# stop a virtual machine but don't deallocate resources (power off)
def stop_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/',
                        vm_name,
                        '/powerOff',
                        '?api-version=', COMP_API])
    return do_post(endpoint, '', access_token)


# update_vm(access_token, subscription_id, resource_group, vm_name, body)
# updates a VM model, that is put an updated virtual machine body, e.g. a sku version
def update_vm(access_token, subscription_id, resource_group, vm_name, body):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachines/', vm_name,
                        '?api-version=', COMP_API])
    return do_put(endpoint, body, access_token)


# update_vmss(access_token, subscription_id, resource_group, vmss_name, body)
# updates a VMSS model, that is put an updated virtual machine scale set body, e.g. a sku version
def update_vmss(access_token, subscription_id, resource_group, vmss_name, body):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '?api-version=', COMP_API])
    return do_put(endpoint, body, access_token)


# upgrade_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids)
# upgrade specific VMs in a virtual machine scale set
def upgrade_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
                        '/manualupgrade?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)
