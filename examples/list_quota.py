import azurerm
import json
import sys

Summary = False

def print_region_quota(region):
    print(region + ':')
    quota = azurerm.get_compute_usage(access_token, subscription_id, region)
    if Summary == False:
        print(json.dumps(quota, sort_keys=False, indent=2, separators=(',', ': ')))
    try:
        for resource in quota['value']:
            if resource['name']['value'] == 'cores':
                print('   Current: ' + str(resource['currentValue']) + ', limit: ' + str(resource['limit']))
                break
    except KeyError:
        print('Invalid data for region: ' + region)

# check for single command argument    
if len(sys.argv) != 2:
    region = 'all'
    Summary = True
else:
    region = sys.argv[1]

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

# print quota
if region == 'all':
    # list locations
    locations = azurerm.list_locations(access_token, subscription_id)
    for location in locations['value']:
        print_region_quota(location['name'])
else:
    print_region_quota(region)

