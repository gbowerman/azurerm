'''list_vms.py - list the virtual machines in a subscription'''
import json
import sys

import azurerm


def main():
    '''Main routine.'''
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

    vmlist = azurerm.list_vms_sub(access_token, subscription_id)
    print(json.dumps(vmlist, sort_keys=False, indent=2, separators=(',', ': ')))
    '''
    for vm in vmlist['value']:
        count += 1
        name = vm['name']
        location = vm['location']
        offer = vm['properties']['storageProfile']['imageReference']['offer']
        sku = vm['properties']['storageProfile']['imageReference']['sku']
        print(''.join([str(count), ': ', name,
                    # ', RG: ', rgname,
                    ', location: ', location,
                    ', OS: ', offer, ' ', sku]))
    '''


if __name__ == "__main__":
    main()
