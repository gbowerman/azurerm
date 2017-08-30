'''list_vm_images.py - list the VM images for a given subscription'''
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

    count = 0
    vmimglist = azurerm.list_vm_images_sub(access_token, subscription_id)
    print(json.dumps(vmimglist, sort_keys=False, indent=2, separators=(',', ': ')))

    for vm_image in vmimglist['value']:
        count += 1
        name = vm_image['name']
        location = vm_image['location']
        offer = vm_image['properties']['storageProfile']['imageReference']['offer']
        sku = vm_image['properties']['storageProfile']['imageReference']['sku']
        print(''.join([str(count), ': ', name,
                       ', location: ', location,
                       ', OS: ', offer, ' ', sku]))


if __name__ == "__main__":
    main()
