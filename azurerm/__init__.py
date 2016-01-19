# azurerm - library for easy Azure Resource Manager calls from Python

from .adalfns        import get_access_token
from .subfns         import list_subscriptions
from .resourcegroups import create_resource_group, delete_resource_group, list_resource_groups
from .computerp      import delete_vm, get_vm, list_vms, restart_vm, start_vm, stop_vm, deallocate_vm, list_vm_scale_sets
from .storagerp      import create_storage_account, delete_storage_account, get_storage_account, list_storage_accounts_sub, list_storage_accounts_rg, get_storage_usage, get_storage_account_keys




