'''instanceviews.py - lists VM instance views for a scale set'''
import azurerm
import sys

import json


def main():
    '''Main routine.'''
    # Load Azure app defaults
    try:
       with open('azurermconfig.json') as configFile:
           configData = json.load(configFile)
    except FileNotFoundError:
       sys.exit("Error: Expecting azurermconfig.json in current folder")

    tenant_id = configData['tenantId']
    app_id = configData['appId']
    app_secret = configData['appSecret']
    subscription_id = configData['subscriptionId']
    rg = configData['resourceGroup']
    vmss = configData['vmssName']

    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    # loop through resource groups
    instances = azurerm.list_vmss_vm_instance_view(access_token, subscription_id, rg, vmss)

    print(json.dumps(instances, sort_keys=False, indent=2, separators=(',', ': ')))


if __name__ == "__main__":
    main()

