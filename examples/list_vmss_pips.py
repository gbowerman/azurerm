import azurerm
import json
import sys

# check for single command argument    
if len(sys.argv) == 3:
    rg = sys.argv[1]
    vmss = sys.argv[2]
else:
      sys.exit('Expecting resource group name and vmss name as arguments.') 
# Load Azure app defaults
try:
    with open('azurermconfig.json') as configFile:
        configData = json.load(configFile)
except FileNotFoundError:
    print("Error: Expecting azurermconfig.json in current folder")
    sys.exit()

tenant_id = configData['tenantId']
app_id = configData['appId']
app_secret = configData['appSecret']
subscription_id = configData['subscriptionId']

access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

public_ips = azurerm.get_vmss_public_ips(access_token, subscription_id, rg, vmss)
print(json.dumps(public_ips, sort_keys=False, indent=2, separators=(',', ': ')))

