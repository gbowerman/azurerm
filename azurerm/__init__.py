# azurerm - library for easy Azure Resource Manager calls from Python

from .adalfns        import get_access_token
from .subfns         import list_subscriptions
from .resourcegroups import create_resource_group, delete_resource_group, list_resource_groups
from .computerp      import list_vm_scale_sets




