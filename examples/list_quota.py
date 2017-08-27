'''list_quota.py - list Compute usage quota for specific regions or all'''
import json
import sys

import azurerm

SUMMARY = False

def print_region_quota(access_token, sub_id, region):
    '''Print the Compute usage quota for a specific region'''
    print(region + ':')
    quota = azurerm.get_compute_usage(access_token, sub_id, region)
    if SUMMARY is False:
        print(json.dumps(quota, sort_keys=False, indent=2, separators=(',', ': ')))
    try:
        for resource in quota['value']:
            if resource['name']['value'] == 'cores':
                print('   Current: ' + str(resource['currentValue']) + ', limit: '
                      + str(resource['limit']))
                break
    except KeyError:
        print('Invalid data for region: ' + region)

def main():
    '''Main routine.'''
    # check for single command argument
    if len(sys.argv) != 2:
        region = 'all'
    else:
        region = sys.argv[1]

    # Load Azure app defaults
    try:
        with open('azurermconfig.json') as config_file:
            config_data = json.load(config_file)
    except FileNotFoundError:
        sys.exit('Error: Expecting azurermconfig.json in current folder')

    tenant_id = config_data['tenantId']
    app_id = config_data['appId']
    app_secret = config_data['appSecret']
    sub_id = config_data['subscriptionId']

    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    # print quota
    if region == 'all':
        # list locations
        locations = azurerm.list_locations(access_token, sub_id)
        for location in locations['value']:
            print_region_quota(access_token, sub_id, location['name'])
    else:
        print_region_quota(access_token, sub_id, region)


if __name__ == "__main__":
    main()
