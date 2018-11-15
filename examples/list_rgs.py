'''list_rgs.py - list Azure resource groups in a subscription'''
import json
import os
import sys

import azurerm

def main():
    '''Main routine.'''
    # if in Azure cloud shell, authenticate using the MSI endpoint
    if 'ACC_CLOUD' in os.environ and 'MSI_ENDPOINT' in os.environ:
        access_token = azurerm.get_access_token_from_cli()
        subscription_id = azurerm.get_subscription_from_cli()
    else: # load service principal details from a config file        
        try:
            with open('azurermconfig.json') as configfile:
                configdata = json.load(configfile)
        except FileNotFoundError:
            sys.exit('Error: Expecting azurermconfig.json in current folder')

        tenant_id = configdata['tenantId']
        app_id = configdata['appId']
        app_secret = configdata['appSecret']
        subscription_id = configdata['subscriptionId']

        # authenticate
        access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    # list resource groups
    resource_groups = azurerm.list_resource_groups(access_token, subscription_id)
    for rgname in resource_groups['value']:
        print(rgname['name'] + ', ' + rgname['location'])
        '''
        rg_details = azurerm.get_resource_group(access_token, subscription_id, rgname['name'])
        print(json.dumps(rg_details, sort_keys=False, indent=2, separators=(',', ': ')))
        '''


if __name__ == "__main__":
    main()