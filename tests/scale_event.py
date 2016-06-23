# To do: change this scale test to not hardcode the sku size
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
rgname = configData['resourceGroup']
vmssname = configData['vmssName']

access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)
input()
scaleoutput = azurerm.scale_vmss(access_token, subscription_id, rgname, vmssname, 'Standard_A1', 'Standard', 98)
print(scaleoutput)
