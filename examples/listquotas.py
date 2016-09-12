import json

import azurerm

# Load Azure app defaults
try:
    with open('azurermconfig.json') as configFile:
        configData = json.load(configFile)
except FileNotFoundError:
    print("Error: Expecting vmssConfig.json in current folder")
    sys.exit()

tenant_id = configData['tenantId']
app_id = configData['appId']
app_secret = configData['appSecret']
subscription_id = configData['subscriptionId']

access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

# list locations
locations = azurerm.list_locations(access_token, subscription_id)

# print quota
for location in locations['value']:
    locationStr = location['name']
    print(locationStr)
    quota = azurerm.get_compute_usage(access_token, subscription_id, locationStr)
    # if locationStr == 'westus' or locationStr == 'southindia' or locationStr == 'centralindia' or locationStr == 'westindia':
    if locationStr != 'southeastasia':
        continue
    print(json.dumps(quota, sort_keys=False, indent=2, separators=(',', ': ')))
    for resource in quota['value']:
        if resource['name']['value'] == 'cores':
            print('Current: ' + str(resource['currentValue']) + ', limit: ' + str(resource['limit']))
            break
