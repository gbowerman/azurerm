import azurerm
import json

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
    # print(locationStr)
    print(json.dumps(location, sort_keys=False, indent=2, separators=(',', ': ')))

    


