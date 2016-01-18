# computerp.py - azurerm functions for the Microsoft.Compute resource provider

from .settings import azure_rm_endpoint, BASEAPI, VMSSAPI
from .restfns import do_delete, do_get, do_put

# list_vm_scale_sets(access_token, subscription_id, resource_group)
def list_vm_scale_sets(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
                         '/subscriptions/', subscription_id,
						 '/resourceGroups/', resource_group,
						 '/providers/Microsoft.Compute/virtualMachineScaleSets/',
						 '?api-version=', VMSSAPI])
    return do_get(endpoint, access_token)