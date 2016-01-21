# azurerm - library for easy Azure Resource Manager calls from Python

from .adalfns        import get_access_token
from .subfns         import list_subscriptions
from .resourcegroups import create_resource_group, delete_resource_group, list_resource_groups
from .computerp      import delete_vm, get_vm, list_vms, restart_vm, start_vm, stop_vm, deallocate_vm, delete_vm_scale_set, delete_vmss_vm, get_vmss, get_vmss_instance_view, list_vm_scale_sets, list_vmss_vms, get_vmss_vm, get_vmss_vm_instance_view, get_vmss_nics, get_vmss_vm_nics, start_vmss, stopdealloc_vmss, start_vmss_vm, stopdealloc_vmss_vm, restart_vmss, restart_vmss_vm, poweroff_vmss, poweroff_vmss_vm, scale_vmss
from .storagerp      import create_storage_account, delete_storage_account, get_storage_account, list_storage_accounts_sub, list_storage_accounts_rg, get_storage_usage, get_storage_account_keys
from .vmimages import list_publishers, list_offers, list_skus


