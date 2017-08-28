'''list_storage.py - list storage account details for a subscription'''
import json
import sys

import azurerm


def rgfromid(idstr):
    '''get resource group name from the id string'''
    rgidx = idstr.find('resourceGroups/')
    providx = idstr.find('/providers/')
    return idstr[rgidx + 15:providx]

def main():
    '''main routine'''
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

    # list storage accounts per sub
    sa_list = azurerm.list_storage_accounts_sub(access_token, subscription_id)
    # print(sa_list)
    for sta in sa_list['value']:
        print(sta['name'] + ', ' + sta['properties']['primaryLocation'] + ', '
              + rgfromid(sta['id']))

    # get storage account quota
    quota_info = azurerm.get_storage_usage(access_token, subscription_id)
    used = quota_info['value'][0]['currentValue']
    limit = quota_info["value"][0]["limit"]
    print('\nUsing ' + str(used) + ' accounts out of ' + str(limit) + '.')


if __name__ == '__main__':
    main()
