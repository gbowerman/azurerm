'''scale_events.py - scale a scale set in or out'''
import json
import sys

import azurerm

def usage():
    '''Return usage and exit.'''
    sys.exit('Usage: python ' + sys.argv[0] + ' rg_name vmss_name capacity')


def main():
    '''main routine'''

    # process arguments
    if len(sys.argv) < 4:
        usage()

    rgname = sys.argv[1]
    vmss_name = sys.argv[2]
    capacity = sys.argv[3]

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

    # get VMSS sku details
    vmss_model = azurerm.get_vmss(access_token, subscription_id, rgname, vmss_name)
    sku_name = vmss_model['sku']['name']
    sku_tier = vmss_model['sku']['tier']

    scaleoutput = azurerm.scale_vmss(access_token, subscription_id, rgname, vmss_name, sku_name,
                                     sku_tier, capacity)
    print(scaleoutput.text)


if __name__ == "__main__":
    main()
