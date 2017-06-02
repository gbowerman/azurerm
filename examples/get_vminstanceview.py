import azurerm
import json
import sys

def usage():
    sys.exit('Usage: python ' + sys.argv[0] + ' rg_name vm_name [vmid]')

# process arguments   
if len(sys.argv) < 3:
    usage()

rg = sys.argv[1]
vm = sys.argv[2]

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

print('Getting VM instance view\n')
instance_view = azurerm.get_vm_instance_view(access_token, subscription_id, rg, vm)
# print(json.dumps(instance_view, sort_keys=False, indent=2, separators=(',', ': ')))
for status in instance_view['statuses']:
    print('Code: ' + status['code'])                                   
    

