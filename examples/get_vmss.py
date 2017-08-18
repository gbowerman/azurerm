'''get_vmss.py - get details about an Azure virtual machine scale set'''
import json
import sys

import azurerm


def usage():
    '''Return usage and exit.'''
    sys.exit('Usage: python ' + sys.argv[0] + ' rg_name vmss_name')


def main():
    '''Main routine.'''
    # process arguments
    if len(sys.argv) < 3:
        usage()

    rgname = sys.argv[1]
    vmss_name = sys.argv[2]

    # Load Azure app defaults
    try:
        with open('azurermconfig.json') as config_file:
            config_data = json.load(config_file)
    except FileNotFoundError:
        sys.exit('Error: Expecting azurermconfig.json in current folder')

    tenant_id = config_data['tenantId']
    app_id = config_data['appId']
    app_secret = config_data['appSecret']
    subscription_id = config_data['subscriptionId']

    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    print('Printing VMSS details\n')
    vmssget = azurerm.get_vmss(
        access_token, subscription_id, rgname, vmss_name)
    name = vmssget['name']
    capacity = vmssget['sku']['capacity']
    location = vmssget['location']
    offer = \
        vmssget['properties']['virtualMachineProfile']['storageProfile']['imageReference']['offer']
    sku = vmssget['properties']['virtualMachineProfile']['storageProfile']['imageReference']['sku']
    print(json.dumps(vmssget, sort_keys=False, indent=2, separators=(',', ': ')))
    print('Name: ' + name + ', capacity: ' + str(capacity) + ', ' + location + ', ' + offer + ', '
          + sku)
    print('Printing VMSS instance view')
    instance_view = azurerm.get_vmss_instance_view(
        access_token, subscription_id, rgname, vmss_name)
    print(json.dumps(instance_view, sort_keys=False,
                     indent=2, separators=(',', ': ')))
    '''
    print('Listing VMSS VMs')
    vmss_vms = azurerm.list_vmss_vms(access_token, subscription_id, rg, vmss)
    print(json.dumps(vmss_vms, sort_keys=False, indent=2, separators=(',', ': ')))
    for vm in vmss_vms['value']:
        instanceId = vm['instanceId']
        vminstance_view = azurerm.get_vmss_vm_instance_view(access_token, subscription_id, rg, vmss,
                                                            instanceId)
        print('VM ' + str(instanceId) + ' instance view')
        print(json.dumps(vminstance_view, sort_keys=False, indent=2, separators=(',', ': ')))
    '''


if __name__ == "__main__":
    main()
