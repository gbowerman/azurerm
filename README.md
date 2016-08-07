# azurerm
Easy to use Python library for Azure Resource Manager.

The azurerm philosophy is ease of use over completeness of API. Rather than support every possible attribute the goal is to provide a set of simple functions for the most common tasks that anyone can extend. 

Note: This is not an official Microsoft library, just some REST wrappers to make it easier to call the Azure REST API. For the official Microsoft Azure library for Python please go here: <a href="https://github.com/Azure/azure-sdk-for-python">https://github.com/Azure/azure-sdk-for-python</a>.

## Installation
1. pip install azurerm
2. To start using, follow the instructions below on authenticating a service principal with Azure Resource Manager.

## Using azurerm
To use this library (and in general to access Azure Resource Manager from a program) you need to register your application with Azure and create a "Service Principal" (an application equivalent of a user). Once you've done this you'll have 3 pieces of information: A tenant ID, an application ID, and an application secret. You will use these to create an authentication token. For more information on how to get this information go here: <a href ="https://azure.microsoft.com/en-us/documentation/articles/resource-group-authenticate-service-principal/">Authenticating a service principal with Azure Resource Manager</a>. See also: <a href="https://msftstack.wordpress.com/2016/01/05/azure-resource-manager-authentication-with-python/">Azure Resource Manager REST calls from Python</a>. Make sure you create a service principal with sufficient access rights, like "Contributor", not "Reader".

A more detailed set of **azurerm** programming examples can be found here: <a href="https://github.com/gbowerman/azurerm/blob/master/examples.md">azurerm Python library programming examples</a>. For even more examples look at the <a href="https://github.com/gbowerman/azurerm/tree/master/tests">azurerm test library</a>.

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
print(json.dumps(rgreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))

# list resource groups
resource_groups = azurerm.list_resource_groups(access_token, subscription_id)
for rg in resource_groups["value"]:
    print(rg["name"] + ', ' + rg["location"] + ', ' + rg["properties"]["provisioningState"])
``` 

#### Example to create a virtual machine
```
import azurerm
impor json

tenant_id = 'your-tenant-id'
application_id = 'your-application-id'
application_secret = 'your-application-secret'

# authenticate
access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

# create resource group
print('Creating resource group: ' + name)
rmreturn = azurerm.create_resource_group(access_token, subscription_id, name, location)
print(rmreturn)

# create storage account
print('Creating storage account: ' + name)
rmreturn = azurerm.create_storage_account(access_token, subscription_id, name, name, location, storage_type='Premium_LRS')
print(rmreturn)

# create VNET
vnetname = name + 'vnet'
print('Creating VNet: ' + vnetname)
rmreturn = azurerm.create_vnet(access_token, subscription_id, name, vnetname, location)
print(rmreturn)
# print(json.dumps(rmreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))
subnet_id = rmreturn.json()['properties']['subnets'][0]['id']
print('subnet_id = ' + subnet_id)

# create public IP address
public_ip_name = name + 'ip'
dns_label = name + 'ip'
print('Creating public IP address: ' + public_ip_name)
rmreturn = azurerm.create_public_ip(access_token, subscription_id, name, public_ip_name, dns_label, location)
print(rmreturn)
ip_id = rmreturn.json()['id']
print('ip_id = ' + ip_id)

# create NIC
nic_name = name + 'nic'
print('Creating NIC: ' + nic_name)
rmreturn = azurerm.create_nic(access_token, subscription_id, name, nic_name, ip_id, subnet_id, location)
print(rmreturn)
nic_id = rmreturn.json()['id']

# create VM
vm_name = name
vm_size = 'Standard_DS1'
publisher = 'Canonical'
offer = 'UbuntuServer'
sku = '16.04.0-LTS'
version = 'latest'
os_uri = 'http://' + name + '.blob.core.windows.net/vhds/osdisk.vhd'
username = 'rootuser'
password = 'myPassw0rd'

print('Creating VM: ' + vm_name)
rmreturn = azurerm.create_vm(access_token, subscription_id, name, vm_name, vm_size, publisher, offer, sku,
                             version, name, os_uri, username, password, nic_id, location)
print(rmreturn)
print(json.dumps(rmreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))
```   

## Functions currently supported
A basic set of infrastructure create, list, query functions are implemented. If you want to add something please send me a PR (don't forget to update this readme too).

### Deployments
```
show_deployment(access_token, subscription_id, resource_group, deployment_name) - show deployment status/details
list_deployment_operations(access_token, subscription_id, resource_group, deployment_name) - list operations involved in a given deployment
```

### Image/Publisher catalog
```
list_offers(access_token, subscription_id, location, publisher) - list available VM image offers from a publisher
list_publishers(access_token, subscription_id, location) - list available image publishers for a location
list_sku_versions(access_token, subscription_id, location, publisher, offer, sku) - list available versions for a given publisher's sku
list_skus(access_token, subscription_id, location, publisher, offer) - list available VM image skus for a publisher offer
```

### Network
```
create_vnet(access_token, subscription_id, resource_group, location, name) # create a VNet with specified name and location
get_load_balancer(access_token, subscription_id, resource_group, lb_name) - get details about a load balancer
get_network_usage(access_token, subscription_id, location) - list network usage and limits for a location
get_public_ip(access_token, subscription_id, resource_group) - get details about the named public ip address
list_load_balancers(access_token, subscription_id) - list the load balancers in a subscription
list_load_balancers_rg(access_token, subscription_id, resource_group) - list the load balancers in a resource group
create_nic(access_token, subscription_id, resource_group, nic_name, public_ip_id, subnet_id, location) # create a network interface
list_nics(access_token, subscription_id) - list the network interfaces in a subscription
list_nics_rg(access_token, subscription_id, resource_group) - list the network interfaces in a resource group
create_public_ip(access_token, subscription_id, resource_group) # list the public ip addresses in a resource group
list_public_ips(access_token, subscription_id, resource_group) - list the public ip addresses in a resource group
list_vnets(access_token, subscription_id) - list the VNETs in a subscription
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
create_storage_account(access_token, subscription_id, rgname, location, storage_type='Standard_LRS') - create a new storage account
delete_storage_account(access_token, subscription_id, rgname) - delete a storage account in the specified resource group
get_storage_account(access_token, subscription_id, rgname) - get details for the specified storage account
get_storage_account_keys(access_token, subscription_id, rgname, account_name) - get the access keys for the specified storage account
get_storage_usage(access_token, subscription_id) - returns storage usage and quota information for the specified subscription
list_storage_accounts_rg(access_token, subscription_id, rgname) - list the storage accounts in the specified resource group
list_storage_accounts_sub(access_token, subscription_id) - list the storage accounts in the specified subscription
```

#### Subscription, location, and access token
```
get_access_token(tenant_id, application_id, application_secret) - get an Azure access token for your application
list_locations(access_token, subscrpition_id) - list available locations for a subscription
list_subscriptions(access_token) - list the available Azure subscriptions for this application  
```

### Template functions
```
deploy_template(access_token, subscription_id, resource_group, deployment_name, template, parameters) - deploy a template referenced by a JSON string, with parameters as a JSON string
deploy_template_uri(access_token, subscription_id, resource_group, deployment_name, template_uri, parameters) - deploy a template referenced by a URI, with parameters as a JSON string
deploy_template_uri_param_uri(access_token, subscription_id, resource_group, deployment_name, template_uri, parameters_uri) - deploy a template with both template and parameters referenced by URIs
```

#### Virtual machines and VM Scale Sets
```
create_vm(access_token, subscription_id, resource_group, vm_name, vm_size, publisher, offer, sku, version,
              storage_account, os_uri, username, password, nic_id, location) # simple vm create function
deallocate_vm(access_token, subscription_id, resource_group, vm_name) - stop-deallocate a virtual machine
delete_vm(access_token, subscription_id, resource_group, vm_name) - delete a virtual machine
delete_vmss(access_token, subscription_id, resource_group, vmss_name) - delete a virtual machine scale set
delete_vmss_vms(access_token, subscription_id, resource_group, vm_ids) - delete a VM in a VM Scale Set
get_compute_usage(access_token, subscription_id, location) - list compute usage and limits for a location
get_vm(access_token, subscription_id, resource_group, vm_name) - get virtual machine details
get_vm_extension(access_token, subscription_id, resource_group, vm_name, extension_name) - get details about a VM extension
get_vmss(access_token, subscription_id, resource_group, vmss_name) - get virtual machine scale set details
get_vmss_instance_view(access_token, subscription_id, resource_group, vmss_name) - get virtual machine scale set instance view
get_vmss_nics(access_token, subscription_id, resource_group, vmss_name) - get NIC details for a VM Scale Set
get_vmss_vm(access_token, subscription_id, resource_group, vmss_name, instance_id) - get individual VMSS VM details
get_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name, instance_id) - get individual VMSS VM instance view
get_vmss_vm_nics(access_token, subscription_id, resource_group, vmss_name, instance_id) - get NIC details for a VMSS VM
list_vms(access_token, subscription_id, resource_group) - list VMs in a resource group
list_vms_sub(access_token, subscription_id) - list the VMs in a subscription
list_vmss(access_token, subscription_id, resource_group) - list the VM Scale Sets in a resource group
list_vmss_sub(access_token, subscription_id) - list the VM Scale Sets in a subscription
list_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name) - list the VMSS VM instance views in a scale set
list_vmss_vms(access_token, subscription_id, resource_group, vmss_name) - list the VMs in a VM Scale Set
restart_vm(access_token, subscription_id, resource_group, vm_name) - restart a virtual machine
restart_vmss(access_token, subscription_id, resource_group, vmss_name) - restart all the VMs in a virtual machine scale set
restart_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_id) - restart VMs in a virtual machine scale set
scale_vmss(access_token, subscription_id, resource_group, vmss_name, size, tier, capacity) - change the instance count of an existing VM Scale Set
start_vm(access_token, subscription_id, resource_group, vm_name) - start a virtual machine
start_vmss(access_token, subscription_id, resource_group, vmss_name) - start all the VMs in a virtual machine scale set
start_vmss_vms(access_token, subscription_id, resource_group, vmss_name, vm_ids) - start VMs in a virtual machine scale set
stop_vm(access_token, subscription_id, resource_group, vm_name) - stop a VM, don't deallocate resources
stopdealloc_vmss(access_token, subscription_id, resource_group, vmss_name) - stop all the VMs in a virtual machine scale set
stopdealloc_vmss_vms(access_token, subscription_id, resource_group, vm_ids) - stop VMs in a virtual machine scale set
poweroff_vmss(access_token, subscription_id, resource_group, vmss_name) - poweroff all the VMs in a virtual machine scale set
poweroff_vmss_vms(access_token, subscription_id, resource_group, vmss_name, vm_ids) - poweroff VMs in a virtual machine scale set
update_vm(access_token, subscription_id, resource_group, vm_name, body) - updates a VM model, that is put an updated virtual machine scale set body
update_vmss(access_token, subscription_id, resource_group, vmss_name, body) - updates a VMSS model, that is put an updated virtual machine scale set body
upgrade_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids) - upgrade a specific VMs a virtual machine scale set
```
