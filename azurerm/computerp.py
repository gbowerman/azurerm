# computerp.py - azurerm functions for the Microsoft.Compute resource provider

from .settings import azure_rm_endpoint, BASEAPI, COMP_API
from .restfns import do_delete, do_get, do_put

# delete_vm(access_token, subscription_id, resource_group, vm_name)
# delete a virtual machine
def delete_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
                         '/subscriptions/', subscription_id,
						 '/resourceGroups/', resource_group,
						 '/providers/Microsoft.Compute/virtualMachines/',
						 vm_name,
						 '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)
	
# get_vm(access_token, subscription_id, resource_group, vm_name)
# get virtual machine details
def get_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
                         '/subscriptions/', subscription_id,
						 '/resourceGroups/', resource_group,
						 '/providers/Microsoft.Compute/virtualMachines/',
						 vm_name,
						 '?api-version=', COMP_API])
    return do_get(endpoint, access_token)

# list_vms(access_token, subscription_id, resource_group)
# list VMs in a resource group
def list_vms(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
                         '/subscriptions/', subscription_id,
						 '/resourceGroups/', resource_group,
						 '/providers/Microsoft.Compute/virtualMachines',
						 '?api-version=', COMP_API])
    return do_get(endpoint, access_token)

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
    return do_post(endpoint, access_token)

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
    return do_post(endpoint, access_token)

# stop_vm(access_token, subscription_id, resource_group, vm_name)
# stop a virtual machine but don't deallocate resources
def stop_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
                         '/subscriptions/', subscription_id,
						 '/resourceGroups/', resource_group,
						 '/providers/Microsoft.Compute/virtualMachines/',
						 vm_name,
						 '/stop',
						 '?api-version=', COMP_API])
    return do_post(endpoint, access_token)

# deallocate_vm(access_token, subscription_id, resource_group, vm_name)
# stop-deallocate a virtual machine
def deallocate_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
                         '/subscriptions/', subscription_id,
						 '/resourceGroups/', resource_group,
						 '/providers/Microsoft.Compute/virtualMachines/', vm_name,
						 '/deallocate',
						 '?api-version=', COMP_API])
    return do_post(endpoint, access_token)

# delete_vm_scale_set(access_token, subscription_id, resource_group, vmss_name)
# delete a virtual machine scale set
def delete_vm_scale_set(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
                         '/subscriptions/', subscription_id,
						 '/resourceGroups/', resource_group,
						 '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
						 '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)

# delete_vmss_vm(access_token, subscription_id, resource_group, vmss_name)
# delete a VM in a VM Scale Set
def delete_vmss_vm(access_token, subscription_id, resource_group, vmss_name, vm_id):
    endpoint = ''.join([azure_rm_endpoint,
                         '/subscriptions/', subscription_id,
						 '/resourceGroups/', resource_group,
						 '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
						 '/virtualMachines/', str(vm_id),
						 '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)
	
# list_vm_scale_sets(access_token, subscription_id, resource_group)
# list VM Scale Sets in a resource group
def list_vm_scale_sets(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
                         '/subscriptions/', subscription_id,
						 '/resourceGroups/', resource_group,
						 '/providers/Microsoft.Compute/virtualMachineScaleSets',
						 '?api-version=', COMP_API])
    return do_get(endpoint, access_token)

# list_vmss_vms(access_token, subscription_id, resource_group, vmss_name)
# list the VMs in a VM Scale Set
def list_vmss_vms(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
                         '/subscriptions/', subscription_id,
						 '/resourceGroups/', resource_group,
						 '/providers/Microsoft.Compute/virtualMachineScaleSets', vmss_name,
						 '?$expand=instanceView&$select=instanceView&api-version=', COMP_API])
    return do_get(endpoint, access_token)	