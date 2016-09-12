# azurerm - library for easy Azure Resource Manager calls from Python

from .adalfns import get_access_token
from .amsrp import check_media_service_name_availability, create_media_service_rg, delete_media_service_rg, \
    list_media_endpoint_keys, list_media_services, list_media_services_rg
from .computerp import create_vm, deallocate_vm, delete_vm, delete_vmss, delete_vmss_vms, get_compute_usage, get_vm, \
    get_vm_extension, get_vmss, get_vmss_instance_view, get_vmss_nics, get_vmss_vm, get_vmss_vm_instance_view, \
    get_vmss_vm_nics, list_as, list_as_sub, list_vm_images_sub, list_vms, list_vms_sub, list_vmss, list_vmss_sub, \
    list_vmss_vm_instance_view, list_vmss_vms, poweroff_vmss, poweroff_vmss_vms, reimage_vmss_vms, restart_vm, \
    restart_vmss, restart_vmss_vms, scale_vmss, start_vm, start_vmss, start_vmss_vms, stop_vm, stopdealloc_vmss, \
    stopdealloc_vmss_vms, update_vm, update_vmss, upgrade_vmss_vms
from .deployments import list_deployment_operations, show_deployment
from .insightsrp import list_autoscale_settings, list_insights_components
from .networkrp import create_nic, create_nsg, create_nsg_rule, create_public_ip, create_vnet, get_lb_nat_rule, \
    get_load_balancer, get_network_usage, get_public_ip, get_vnet, list_lb_nat_rules, list_load_balancers, \
    list_load_balancers_rg, list_nics, list_nics_rg, list_public_ips, list_vnets
from .resourcegroups import create_resource_group, delete_resource_group, list_resource_groups
from .storagerp import create_storage_account, delete_storage_account, get_storage_account, get_storage_account_keys, \
    get_storage_usage, list_storage_accounts_rg, list_storage_accounts_sub
from .subfns import list_locations, list_subscriptions
from .templates import deploy_template, deploy_template_uri, deploy_template_uri_param_uri
from .vmimages import list_offers, list_publishers, list_skus, list_sku_versions
