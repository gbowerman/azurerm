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
resource_group = configData['resourceGroup']

access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)
print(access_token)

# loop through resource groups
count = 0
vmlist = azurerm.list_vms_sub(access_token, subscription_id)
print(json.dumps(vmlist, sort_keys=False, indent=2, separators=(',', ': ')))
'''
for vm in vmlist['value']:
    count += 1
    name = vm['name']
    location = vm['location']
    offer = vm['properties']['storageProfile']['imageReference']['offer']
    sku = vm['properties']['storageProfile']['imageReference']['sku']
    print(''.join([str(count), ': ', name,
                   # ', RG: ', rgname,
                   ', location: ', location,
                   ', OS: ', offer, ' ', sku]))
'''
# get extension details (note the hardcoded values you'll need to change
#extn = azurerm.get_vm_extension(access_token, subscription_id, resource_group, 'MyDockerVm', #'LinuxDiagnostic')
#print(json.dumps(extn, sort_keys=False, indent=2, separators=(',', ': ')))

        
    
