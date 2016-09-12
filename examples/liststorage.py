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


# pull the resource group name from the id string
def rgfromid(idstr):
    rgidx = idstr.find('resourceGroups/')
    providx = idstr.find('/providers/')
    return idstr[rgidx + 15:providx]


access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

# list storage accounts per sub
sa_list = azurerm.list_storage_accounts_sub(access_token, subscription_id)
# print(sa_list)
for sa in sa_list['value']:
    print(sa['name'] + ', ' + sa['properties']['primaryLocation'] + ', ' + rgfromid(sa['id']))

# get storage account quota
quota_info = azurerm.get_storage_usage(access_token, subscription_id)
used = quota_info['value'][0]['currentValue']
limit = quota_info["value"][0]["limit"]
print('\nUsing ' + str(used) + ' accounts out of ' + str(limit) + '.')
