'''delete_rg.py - example script to delete an Azure Resource Group'''
import json
import sys

import azurerm


def usage():
    '''Basic usage function to print usage and exit.'''
    sys.exit('Usage: python ' + sys.argv[0] + ' rg_name')


def main():
    '''Main routine.'''
    # check for single command argument
    if len(sys.argv) != 2:
        usage()

    rgname = sys.argv[1]

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

    # delete a resource group
    rgreturn = azurerm.delete_resource_group(access_token, subscription_id, rgname)
    print(rgreturn)


if __name__ == "__main__":
    main()
