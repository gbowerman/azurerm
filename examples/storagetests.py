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
# resource_group = configData['resourceGroup']
resource_group = 'guyqlen'

access_token = azurerm.get_access_token(
    tenant_id,
    app_id,
    app_secret
)

# create a storage account 
print('Enter storage account name to create.')
saname = input()
location = 'eastus'
sareturn = azurerm.create_storage_account(access_token, subscription_id, resource_group, saname, location)
print(sareturn)

# list storage accounts per sub
sa_list = azurerm.list_storage_accounts_sub(access_token, subscription_id)
print(json.dumps(sa_list, sort_keys=False, indent=2, separators=(',', ': ')))
# for rg in resource_groups["value"]:
#    print(rg["name"] + ', ' + rg["location"] + ', ' + rg["properties"]["provisioningState"])

print('Press Enter to continue and list accounts in RG.')
input()

# list storage accounts in rg
sa_list = azurerm.list_storage_accounts_rg(access_token, subscription_id, resource_group)
print(json.dumps(sa_list, sort_keys=False, indent=2, separators=(',', ': ')))

print('Storage account details...')

# get storage account details
sa_info = azurerm.get_storage_account(access_token, subscription_id, resource_group, saname)
print(json.dumps(sa_info, sort_keys=False, indent=2, separators=(',', ': ')))

print('Storage account quota...')

# get storage account quota
quota_info = azurerm.get_storage_usage(access_token, subscription_id)
print(json.dumps(quota_info, sort_keys=False, indent=2, separators=(',', ': ')))

print('Storage account keys...')

# get storage account keys
keys = azurerm.get_storage_account_keys(access_token, subscription_id, resource_group, saname)
print(keys.text)

# delete storage_account
# print('Press Enter to delete account.')
# input()
# rgreturn = azurerm.delete_storage_account(access_token, subscription_id, resource_group, saname)
# print(rgreturn)

