'''list_pubs.py - list Azure publishers'''
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
        sys.exit("Error: Expecting azurermonfig.json in current folder")

    tenant_id = config_data['tenantId']
    app_id = config_data['appId']
    app_secret = config_data['appSecret']
    subscription_id = config_data['subscriptionId']

    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)
    '''
    pubs = azurerm.list_publishers(access_token, subscription_id, 'southeastasia')
    for pub in pubs:
    #    print(json.dumps(pub, sort_keys=False, indent=2, separators=(',', ': ')))
        print(pub['name'])

    offers = azurerm.list_offers(access_token, subscription_id, 'southeastasia', 'rancher')
    for offer in offers:
        print(json.dumps(offer, sort_keys=False, indent=2, separators=(',', ': ')))

    skus = azurerm.list_skus(access_token, subscription_id, 'southeastasia', 'rancher', 'rancheros')
    for sku in skus:
        print(sku['name'])
    '''
    #print('Versions for CoreOS:')
    versions = azurerm.list_sku_versions(access_token, subscription_id, 'eastasia', 'CoreOS',
                                         'CoreOS', 'Stable')
    for version in versions:
        print(version['name'])

if __name__ == "__main__":
    main()
