# azurerm - change log

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


