#!/usr/bin/env python

"""
Copyright (c) 2016, Guy Bowerman
Description: Simple Azure Resource Manager Python library
License: MIT (see LICENSE.txt file for details)
"""

# azurerm - library for easy Azure Resource Manager calls from Python

from .adalfns        import get_access_token
from .subfns         import list_subscriptions, list_locations
from .resourcegroups import create_resource_group, delete_resource_group, list_resource_groups
from .deployments    import show_deployment
from .computerp      import delete_vm, get_vm, list_vms, restart_vm, start_vm, stop_vm, deallocate_vm, delete_vm_scale_set, delete_vmss_vm, get_vmss, get_vmss_instance_view, list_vm_scale_sets, list_vmss_vms, get_vmss_vm, get_vmss_vm_instance_view, get_vmss_nics, get_vmss_vm_nics, start_vmss, stopdealloc_vmss, start_vmss_vm, stopdealloc_vmss_vm, restart_vmss, restart_vmss_vm, poweroff_vmss, poweroff_vmss_vm, scale_vmss, get_compute_usage
from .storagerp      import create_storage_account, delete_storage_account, get_storage_account, list_storage_accounts_sub, list_storage_accounts_rg, get_storage_usage, get_storage_account_keys
from .networkrp      import get_network_usage, list_vnets, list_nics, list_nics_rg, list_load_balancers, list_load_balancers_rg, get_load_balancer, list_public_ips, get_public_ip
from .insightsrp     import list_insights_components, list_autoscale_settings
from .vmimages       import list_publishers, list_offers, list_skus, list_sku_versions
from .templates      import deploy_template, deploy_template_uri, deploy_template_uri_param_uri


