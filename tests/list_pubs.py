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
'''
pubs = azurerm.list_publishers(access_token, subscription_id, 'southeastasia')

for pub in pubs:
    print(pub['name'])

offers = azurerm.list_offers(access_token, subscription_id, 'southeastasia', 'MicrosoftWindowsServer')
for offer in offers:
    print(offer['name'])

skus = azurerm.list_skus(access_token, subscription_id, 'southeastasia', 'MicrosoftWindowsServer', 'WindowsServer')
for sku in skus:
    print(sku['name'])
'''
#versions = azurerm.list_sku_versions(access_token, subscription_id, 'eastus', 'MicrosoftWindowsServer', 'WindowsServer', '2012-R2-Datacenter')
versions = azurerm.list_sku_versions(access_token, subscription_id, 'eastus', 'Canonical', 'UbuntuServer', '15.04')
for version in versions:
    print(version['name'])

