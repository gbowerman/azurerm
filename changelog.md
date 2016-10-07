# azurerm - change log

### v0.6.12 (Oct 7 2016):
- Added create_vmss() function + unit test. This function creates a VM Scale Set. Initially it only accepts a password rather than a cert. There are a few assumptions made about load balancer configuration too. For example see [create_vmss.py](./tree/master/examples/create_vmss.py).
- Started using a change log :-)

### Earlier versions

The most recent enhancements before 0.6.12 include the following:

- Added create_vm() function to create a virtual machine.
- Added create_lb_with_nat_pool() function to create a load balancer which can be used with VM Scale Sets.
- Added unit tests, with the goal that all new functions should include a unit test. See [test/](./tree/master/test) for more details. These are also useful for seeing how to call functions.
- Added delete_vnet().
- Fixed a bug with stop_vm().
- Added pagination support for list functions.
- Added media services support (msleal).
- Added insights metrics support (gatneil).
- Added ability to list deployment operations (rcarmo).


