# azurerm
Easy to use Python library for Azure Resource Manager.

The azurerm philosophy is ease of use over completeness of API. Rather than support every possible attribute the goal is to provide a set of simple functions for the most common tasks. 

Note: This is not an official Microsoft library, just some REST wrappers to make it easier to call the Azure REST API. For the official Microsoft Azure library for Python please go here: <a href="https://github.com/Azure/azure-sdk-for-python">https://github.com/Azure/azure-sdk-for-python</a>.

## Installation
1. pip install azurerm
2. To start using, follow the instructions below on authenticating a service principal with Azure Resource Manager.

## Using azurerm
To use this library (and in general to access Azure Resource Manager from a program) you need to register your application with Azure and create a "Service Principal" (an application equivalent of a user). Once you've done this you'll have 3 pieces of information: A tenant ID, an application ID, and an application secret. You will use these to create an authentication token. For more information on how to get this information go here: <a href ="https://azure.microsoft.com/en-us/documentation/articles/resource-group-authenticate-service-principal/">Authenticating a service principal with Azure Resource Manager</a>. See also: <a href="https://msftstack.wordpress.com/2016/01/05/azure-resource-manager-authentication-with-python/">Azure Resource Manager REST calls from Python</a>.

A more complete list of **azurerm** programming examples can be found here: <a href="https://github.com/gbowerman/azurerm/blob/master/examples.md">azurerm Python library programming examples</a>.

#### Example to list Azure subscriptions, create a Resource Group, list Resource Groups
```
import azurerm

tenant_id = 'your-tenant-id'
application_id = 'your-application-id'
application_secret = 'your-application-secret'

# create an authentication token
access_token = azurerm.get_access_token(
    tenant_id,
    application_id,
    application_secret
)

# list subscriptions
subscriptions = azurerm.list_subscriptions(access_token)
for sub in subscriptions["value"]:
    print(sub["displayName"] + ': ' + sub["subscriptionId"])

# select the first subscription
subscription_id = subscriptions["value"][0]["subscriptionId"]

# create a resource group
print('Enter Resource group name to create.')
rgname = input()
location = 'southeastasia'
rgreturn = azurerm.create_resource_group(access_token, subscription_id, rgname, location)
print(rgreturn)

# list resource groups
resource_groups = azurerm.list_resource_groups(access_token, subscription_id)
for rg in resource_groups["value"]:
    print(rg["name"] + ', ' + rg["location"] + ', ' + rg["properties"]["provisioningState"])
```    
## Functions currently supported
Basic resource group, storage and VM/VMSS functions are implemented. Network functions, create VM and general template deploy need filling out. If you want to add something please send me a PR (don't forget to update this readme too).

### Deployments
```
show_deployment(access_token, subscription_id, resource_group, deployment_name) - show deployment status/details
```

### Image/Publisher catalog
```
list_publishers(access_token, subscription_id, location) - list available image publishers for a location
list_offers(access_token, subscription_id, location, publisher) - list available VM image offers from a publisher
list_skus(access_token, subscription_id, location, publisher, offer) - list available VM image skus for a publisher offer
list_sku_versions(access_token, subscription_id, location, publisher, offer, sku) - list available versions for a given publisher's sku
```

### Network
```
list_vnets(access_token, subscription_id) - list the VNETs in a subscription
list_nics(access_token, subscription_id) - list the network interfaces in a subscription
list_nics_rg(access_token, subscription_id, resource_group) - list the network interfaces in a resource group	
list_load_balancers(access_token, subscription_id) - list the load balancers in a subscription
list_load_balancers_rg(access_token, subscription_id, resource_group) - list the load balancers in a resource group
get_load_balancer(access_token, subscription_id, resource_group, lb_name) - get details about a load balancer
list_public_ips(access_token, subscription_id, resource_group) - list the public ip addresses in a resource group	
get_public_ip(access_token, subscription_id, resource_group) - get details about the named public ip address
get_network_usage(access_token, subscription_id, location) - list network usage and limits for a location
```

### Insights
```
list_autoscale_settings(access_token, subscription_id) - list the autoscale settings in a subscription_id
list_insights_components(access_token, subscription_id, resource_group) - list the Microsoft Insights components in a resource group	
```

#### Resource groups
```
create_resource_group(access_token, subscription_id, rgname, location) - create a resource group in the specified location  
delete_resource_group(access_token, subscription_id, rgname) - delete the named resource group  
list_resource_groups(access_token, subscription_id) - list the resource groups in your subscription  
```

#### Storage
```
create_storage_account(access_token, subscription_id, rgname, location) - create a new storage account
delete_storage_account(access_token, subscription_id, rgname) - delete a storage account in the specified resource group
get_storage_account(access_token, subscription_id, rgname) - get details for the specified storage account
list_storage_accounts_rg(access_token, subscription_id, rgname) - list the storage accounts in the specified resource group
list_storage_accounts_sub(access_token, subscription_id) - list the storage accounts in the specified subscription
get_storage_account_keys(access_token, subscription_id, rgname, account_name) - get the access keys for the specified storage account
get_storage_usage(access_token, subscription_id) - returns storage usage and quota information for the specified subscription
```

#### Subscription, location, and access token
```
get_access_token(tenant_id, application_id, application_secret) - get an Azure access token for your application  
list_subscriptions(access_token) - list the available Azure subscriptions for this application  
list_locations(access_token, subscrpition_id) - list available locations for a subscription
```

### Template functions
```
deploy_template_uri_param_uri(access_token, subscription_id, resource_group, deployment_name, template_uri, parameters_uri) - deploy a template with both template and parameters referenced by URIs
deploy_template_uri(access_token, subscription_id, resource_group, deployment_name, template_uri, parameters) - deploy a template referenced by a URI, with parameters as a JSON string
deploy_template(access_token, subscription_id, resource_group, deployment_name, template, parameters) - deploy a template referenced by a JSON string, with parameters as a JSON string
```

#### Virtual machines and VM Scale Sets
```
delete_vm(access_token, subscription_id, resource_group, vm_name) - delete a virtual machine
get_vm(access_token, subscription_id, resource_group, vm_name) - get virtual machine details
list_vms(access_token, subscription_id, resource_group) - list VMs in a resource group
restart_vm(access_token, subscription_id, resource_group, vm_name) - restart a virtual machine
start_vm(access_token, subscription_id, resource_group, vm_name) - start a virtual machine
stop_vm(access_token, subscription_id, resource_group, vm_name) - stop a VM, don't deallocate resources
deallocate_vm(access_token, subscription_id, resource_group, vm_name) - stop-deallocate a virtual machine
delete_vm_scale_set(access_token, subscription_id, resource_group, vmss_name) - delete a virtual machine scale set
delete_vmss_vm(access_token, subscription_id, resource_group, vmss_name) - delete a VM in a VM Scale Set
list_vmss_vms(access_token, subscription_id, resource_group, vmss_name) - list the VMs in a VM Scale Set
list_vm_scale_sets(access_token, subscription_id, rgname) - list the VM Scale Sets in a resource group
get_vm_extensionaccess_token, subscription_id, resource_group, vm_name, extension_name) - get details about a VM extension
get_vmss(access_token, subscription_id, resource_group, vmss_name) - get virtual machine scale set details
get_vmss_instance_view(access_token, subscription_id, resource_group, vmss_name) - get virtual machine scale set instance view
get_vmss_vm(access_token, subscription_id, resource_group, vmss_name, instance_id) - get individual VMSS VM details
get_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name, instance_id) - get individual VMSS VM instance view
get_vmss_nics(access_token, subscription_id, resource_group, vmss_name) - get individual VMSS VM instance view
get_vmss_vm_nics(access_token, subscription_id, resource_group, vmss_name, instance_id) - get individual VMSS VM instance view
start_vmss(access_token, subscription_id, resource_group, vmss_name) - start all the VMs in a virtual machine scale set
start_vmss_vm(access_token, subscription_id, resource_group, vmss_name) - start a VM in a virtual machine scale set
stopdealloc_vmss(access_token, subscription_id, resource_group, vmss_name) - stop all the VMs in a virtual machine scale set
stopdealloc_vmss_vm(access_token, subscription_id, resource_group, vmss_name) - stop a VM in a virtual machine scale set
restart_vmss(access_token, subscription_id, resource_group, vmss_name) - restart all the VMs in a virtual machine scale set
restart_vmss_vm(access_token, subscription_id, resource_group, vmss_name, instance_id) - restart all the VMs in a virtual machine scale set
poweroff_vmss(access_token, subscription_id, resource_group, vmss_name) - poweroff all the VMs in a virtual machine scale set
poweroff_vmss_vm(access_token, subscription_id, resource_group, vmss_name, instance_id) - poweroff all the VMs in a virtual machine scale set
scale_vmss(access_token, subscription_id, resource_group, vmss_name, size, tier, capacity) - change the instance count of an existing VM Scale Set
get_compute_usage(access_token, subscription_id, location) - list compute usage and limits for a location
```