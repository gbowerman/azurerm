'''list_vmss_vms.py - list the VMs in a VM scale set'''
import json
import sys

import azurerm


def usage():
    '''Return usage and exit.'''
    sys.exit('Usage: python ' + sys.argv[0] + ' rg_name vmss_name')


def main():
    '''main routine'''

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
        sys.exit('Error: Expecting azurermonfig.json in current folder')

    tenant_id = config_data['tenantId']
    app_id = config_data['appId']
    app_secret = config_data['appSecret']
    subscription_id = config_data['subscriptionId']

    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    instanceviewlist = azurerm.list_vmss_vm_instance_view(access_token, subscription_id, rgname,
                                                          vmss_name)
    for vmi in instanceviewlist['value']:
        instance_id = vmi['instanceId']
        upgrade_domain = vmi['properties']['instanceView']['platformUpdateDomain']
        fault_domain = vmi['properties']['instanceView']['platformFaultDomain']
        print('Instance ID: ' + instance_id + ', UD: ' + str(upgrade_domain) + ', FD: '
              + str(fault_domain))
        # print(json.dumps(instanceviewlist, sort_keys=False, indent=2, separators=(',', ': ')))


if __name__ == "__main__":
    main()
