'''get_vminstanceview.py - returns the instance view for an Azure VM'''
import json
import sys

import azurerm


def usage():
    '''Return usage and exit.'''
    sys.exit('Usage: python ' + sys.argv[0] + ' rg_name vm_name')


def main():
    '''Main routine.'''
    # process arguments
    if len(sys.argv) < 3:
        usage()

    rgname = sys.argv[1]
    vm_name = sys.argv[2]

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

    print('Getting VM instance view\n')
    instance_view = azurerm.get_vm_instance_view(
        access_token, subscription_id, rgname, vm_name)
    print(json.dumps(instance_view, sort_keys=False,
                     indent=2, separators=(',', ': ')))
    # for status in instance_view['statuses']:
    #    print('Code: ' + status['code'])


if __name__ == "__main__":
    main()
