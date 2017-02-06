# azurerm - change log

### v0.7.15 (Feb 5 2017):
- BREAKING CHANGE: create_vmss() - storage containers argument removed
- Fix create_vmss() and create it with managed disks
- Fix examples\create_vmss()
- Update Compute test

### v0.7.14 (Feb 5 2017):
- BREAKING CHANGE: create_vm() - storage account argument removed, OS URI parameter removed
- Fix create_vm() and create it with managed disks
- Add list_vnet_rg() to list VNETs in a resource group
- Fix examples\create_vm()
- Add new examples\jumpbox() to drop a jumpbox vm into existing VNET
- Update Compute test

### v0.7.13 (Jan 29 2017):
- Set User-Agent in the Azure REST headers.

### v0.7.12 (Jan 26 2017):
- Add Availability Set support: create_as(), get_as(), delete_as(). Thanks @KineticHub
- See also create_as.py in examples.

### v0.7.11 (Jan 22 2017):
- Add paginated list_vmss_vm_instance_view_pg() function to make it easier to get a smaller list of instances views at a time

### v0.7.10 (Jan 20 2017):
- Fix adal deprecation issue

### v0.7.9 (Jan 19 2017):
- Update BASE_API for Resource Manager calls to 2016-09-01

### v0.7.8 (Jan 18 2017):
- Update list_vmss_vm_instance_view() to use paginated API
- Set COMP_API version to be 2016-04-30-preview

### v0.7.7 (Jan 10 2017):
- Add update_load_balancer() - makes it easy to change load balancer configuration
- Add vip_swap.py to examples 

### v0.7.6 (Jan 6 2017):
- Update COMPUTE_API to 2016-08-30
- Adds ability to update customData property of a VM scale set

### v0.7.5 (Dec 9 2016):
- Update NETWORK_API to 2016-09-01
- This change fixes get_vmss_nics()

### v0.7.4 (Dec 5 2016):
- Updated Microsoft.Compute API version to 2016-04-30-preview
- This is to support preview scale set features like managed disks and large scale sets

### v0.7.3 (Nov 19 2016):
- Added list_vmss_skus(access_token, subscription_id, resource_group, vmss_name)
- list the VM skus available for a VM Scale Set

### v0.7.2 (Oct 31 2016):
- Refactored azure media services functions (finishing the changes in 0.7.0)

### v0.7.1 (Oct 31 2016):
- BREAKING CHANGE: to support sha key support in create_vm() and create_vmss() 
- These function have new positions for user/password, and the new public_key parameter
- You can now provide a public_key OR a password (or both if you want)
- New usage: 
create_vm(access_token, subscription_id, resource_group, vm_name, vm_size, publisher, offer, sku, version, storage_account, os_uri, nic_id, location, username='azure', password=None, public_key=None)
- it is recommended to pass in the username, password and/or public_key as named parameters to avoid confusion. 

- New usage: 
create_vmss(access_token, subscription_id, resource_group, vmss_name, vm_size, capacity, publisher, offer, sku, version, storage_container_list, subnet_id, be_pool_id, lb_pool_id, location, username='azure', password=None, public_key=None, overprovision='true', upgradePolicy='Manual') 
- it is recommended to pass in any optional parameters after username as named parameters to avoid confusion.

### v0.7.0 (Oct 31 2016):
- All create functions have been refactored to make them easier to maintain.
- Previously a PUT REST call had its JSON body constructed using join() to concatenate a string. This was cumbersome and messy to update.
- Now a Python dictionary is constructed for the body, which is then converted to a string with json.dumps() 
- In future it will be easier to create functions without messing with large join() strings.

### v0.6.17 (Oct 29 2016):
- Add create_autoscale_rule() and create_autoscale_settings(). 
- The output from create_autoscale_rule() is a dictionary object. Create a list of these rules and pass the list as an argument to create_autoscale setttings().
- Pass in the name of an existing VM scale set to create_autoscale_settings.
- Added unit tests for insights. See insights_tests.py in [test/](./test) for an example of how to call these new functions.


### v0.6.16 (Oct 23 2016):
- Added list_vm_instance_view() to get instance details about the VMs in a resource group


### v0.6.15 (Oct 23 2016):
- Added get_vm_instance_view() to get instance state details about a VM


### v0.6.13 (Oct 14 2016):
- Added Azure Container Services support + unit tests.

```
  create_container_service(access_token, subscription_id, resource_group, service_name,
    agent_count, agent_vm_size, agent_dns, master_dns, admin_user, public_key, location,
    master_count=3, orchestrator='DCOS') # create a new container service 
  delete_container_service(access_token, subscription_id, resource_group, container_service_name) # delete a named container service
  get_container_service(access_token, subscription_id, resource_group, service_name) # get details about an Azure Container Server
  list_acs_operations(access_token) # list available Container Server operations
  list_container_services(access_token, subscription_id, resource_grou) # list the container services in a resource group
  list_container_services_sub(access_token, subscription_id) # list the container services in a subscription
```

### v0.6.12 (Oct 7 2016):
- Added create_vmss() function + unit test. This function creates a VM Scale Set. Initially it only accepts a password rather than a cert. There are a few assumptions made about load balancer configuration too. For example see [create_vmss.py](./examples/create_vmss.py).
- Started using a change log :-)

### Earlier versions

The most recent enhancements before 0.6.12 include the following:

- Added create_vm() function to create a virtual machine.
- Added create_lb_with_nat_pool() function to create a load balancer which can be used with VM Scale Sets.
- Added unit tests, with the goal that all new functions should include a unit test. See [test/](./test) for more details. These are also useful for seeing how to call functions.
- Added delete_vnet().
- Fixed a bug with stop_vm().
- Added pagination support for list functions.
- Added media services support (msleal).
- Added insights metrics support (gatneil).
- Added ability to list deployment operations (rcarmo).


