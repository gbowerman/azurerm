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
rg = configData['resourceGroup']
vmss = configData['vmssName']

access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

# get metric definitions
provider = 'Microsoft.Compute'
resource_type = 'virtualMachineScaleSets'

metric_definitions = azurerm.list_metric_definitions_for_resource(access_token, subscription_id, rg, \
    provider, resource_type, vmss)

print(json.dumps(metric_definitions, sort_keys=False, indent=2, separators=(',', ': ')))

metrics = azurerm.get_metrics_for_resource(access_token, subscription_id, rg, \
    provider, resource_type, vmss)

print(json.dumps(metrics, sort_keys=False, indent=2, separators=(',', ': ')))