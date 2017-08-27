'''insightstests.py - list insights settings for each Azure resource group'''
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
        print("Error: Expecting azurermconfig.json in current folder")
        sys.exit()

    tenant_id = config_data['tenantId']
    app_id = config_data['appId']
    app_secret = config_data['appSecret']
    subscription_id = config_data['subscriptionId']

    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    # list autoscale settings
    auto_settings = azurerm.list_autoscale_settings(access_token, subscription_id)
    print(auto_settings)
    for auto_setting in auto_settings['value']:
        print(auto_setting['name'] + ', ' + auto_setting['location'])
        print(auto_setting['properties']['profiles'])

    # loop through resource groups
    resource_groups = azurerm.list_resource_groups(access_token, subscription_id)
    for rgs in resource_groups["value"]:
        rgname = rgs["name"]
        insights_comp = azurerm.list_insights_components(access_token, subscription_id, rgname)
        if len(insights_comp) > 0:
            print(insights_comp)


if __name__ == "__main__":
    main()
