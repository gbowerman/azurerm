'''vmssops.py - example program to show running operations on scale set VMs'''
import json
import sys

import azurerm


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
    resource_group = config_data['resourceGroup']
    vmssname = config_data['vmssName']

    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    # delete vmss vm id #1
    #vm_ids = '["1"]'
    #result = azurerm.delete_vmss_vms(access_token, subscription_id, resource_group, vmssname,
    #                                 vm_ids)
    # print(result)

    # restart vmss vm id's #2, #3
    #vm_ids = '["2", "3"]'
    #result = azurerm.restart_vmss_vms(access_token, subscription_id, resource_group, vmssname,
    #                                  vm_ids)
    # print(result)

    # poweroff some vmss vm's
    vm_ids = '["7", "9"]'
    result = azurerm.poweroff_vmss_vms(access_token, subscription_id, resource_group, vmssname,
                                       vm_ids)
    print(result)

    # start vmss vm id's #2, #3
    #vm_ids = '["2", "3"]'
    #result = azurerm.start_vmss_vms(access_token, subscription_id, resource_group, vmssname,
    #                                vm_ids)
    # print(result)


if __name__ == '__main__':
    main()
