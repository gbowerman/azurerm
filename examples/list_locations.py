'''list_locations.py - list Azure locations'''
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
        sys.exit("Error: Expecting azurermconfig.json in current folder")

    tenant_id = config_data['tenantId']
    app_id = config_data['appId']
    app_secret = config_data['appSecret']
    subscription_id = config_data['subscriptionId']

    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    # list locations
    locations = azurerm.list_locations(access_token, subscription_id)

    for location in locations['value']:
        print(location['name']
              + ', Display Name: ' + location['displayName']
              + ', Coords: ' + location['latitude']
              + ', ' + location['longitude'])


if __name__ == "__main__":
    main()
