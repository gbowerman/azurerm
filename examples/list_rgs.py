'''list_rgs.py - list Azure resource groups in a subscription'''
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
        sys.exit("Error: Expecting vmssConfig.json in current folder")

    tenant_id = config_data['tenantId']
    app_id = config_data['appId']
    app_secret = config_data['appSecret']
    sub_id = config_data['subscriptionId']

    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    # list resource groups
    resource_groups = azurerm.list_resource_groups(access_token, sub_id)
    for rgname in resource_groups['value']:
        print(rgname['name'] + ', ' + rgname['location'] + ', '
              + rgname['properties']['provisioningState'])
        print('Resource group details..')
        rg_details = azurerm.get_resource_group(access_token, sub_id, rgname['name'])
        print(json.dumps(rg_details, sort_keys=False, indent=2, separators=(',', ': ')))


if __name__ == "__main__":
    main()
