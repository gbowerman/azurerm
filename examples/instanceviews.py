'''instanceviews.py - lists VM instance views for a scale set'''
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
    vmss = sys.argv[2]

    # Load Azure app defaults
    try:
        with open('azurermconfig.json') as config_file:
            config_data = json.load(config_file)
    except FileNotFoundError:
        sys.exit("Error: Expecting azurermconfig.json in current folder")

    tenant_id = config_data['tenantId']
    app_id = config_data['appId']
    app_secret = config_data['appSecret']
    subscription_id = config_data['subscriptionId']

    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    # loop through resource groups
    instances = azurerm.list_vmss_vm_instance_view(access_token, subscription_id, rgname, vmss)

    print(json.dumps(instances, sort_keys=False, indent=2, separators=(',', ': ')))


if __name__ == "__main__":
    main()
