'''list_vmss.py - list the scale sets in a subscription'''
import json
import sys

import azurerm


def main():
    '''main reoutine'''
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

    # list the VMs
    vmsslist = azurerm.list_vmss_sub(access_token, subscription_id)
    print(json.dumps(vmsslist, sort_keys=False, indent=2, separators=(',', ': ')))

    '''
    for vmss in vmsslist['value']:
        # print(json.dumps(vmss, sort_keys=False, indent=2, separators=(',', ': ')))
        print(vmss['name'])
    '''

if __name__ == "__main__":
    main()
