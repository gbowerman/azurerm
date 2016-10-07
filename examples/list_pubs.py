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

#pubs = azurerm.list_publishers(access_token, subscription_id, 'southeastasia')
'''
skus = azurerm.list_skus(access_token, subscription_id, 'southeastasia', 'MicrosoftWindowsServer', 'WindowsServer')
# skus = azurerm.list_skus(access_token, subscription_id, 'southeastasia', 'Canonical', 'UbuntuServer')
for sku in skus:
    print(sku['name'])
'''
#print('Versions for CoreOS:')
#versions = azurerm.list_sku_versions(access_token, subscription_id, 'southeastasia', 'Canonical', 'UbuntuServer', '16.04.0-LTS')
# versions = azurerm.list_sku_versions(access_token, subscription_id, 'southeastasia', 'Canonical', 'UbuntuServer', '15.10')
versions = azurerm.list_sku_versions(access_token, subscription_id, 'eastasia', 'CoreOS', 'CoreOS', 'Stable')
for version in versions:
    print(version['name'])