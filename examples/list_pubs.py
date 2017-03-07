import azurerm
import json

# Load Azure app defaults
try:
   with open('azurermconfig.json') as configFile:    
      configData = json.load(configFile)
except FileNotFoundError:
   print("Error: Expecting azurermonfig.json in current folder")
   sys.exit()
   
tenant_id = configData['tenantId']
app_id = configData['appId']
app_secret = configData['appSecret']
subscription_id = configData['subscriptionId']

access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)
'''
pubs = azurerm.list_publishers(access_token, subscription_id, 'southeastasia')
for pub in pubs:
#    print(json.dumps(pub, sort_keys=False, indent=2, separators=(',', ': ')))
    print(pub['name'])

offers = azurerm.list_offers(access_token, subscription_id, 'southeastasia', 'rancher')
for offer in offers:
    print(json.dumps(offer, sort_keys=False, indent=2, separators=(',', ': ')))

#skus = azurerm.list_skus(access_token, subscription_id, 'southeastasia', 'MicrosoftWindowsServer', 'WindowsServer')
# skus = azurerm.list_skus(access_token, subscription_id, 'southeastasia', 'Canonical', 'UbuntuServer')
skus = azurerm.list_skus(access_token, subscription_id, 'southeastasia', 'rancher', 'rancheros')
for sku in skus:
    print(sku['name'])
'''
#print('Versions for CoreOS:')
versions = azurerm.list_sku_versions(access_token, subscription_id, 'southeastasia', 'Canonical', 'UbuntuServer', '16.04-LTS')
#versions = azurerm.list_sku_versions(access_token, subscription_id, 'eastasia', 'CoreOS', 'CoreOS', 'Stable')
# versions = azurerm.list_sku_versions(access_token, subscription_id, 'eastasia', 'rancher', 'rancheros', 'os')
for version in versions:
    print(version['name'])
