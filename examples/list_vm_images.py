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

count = 0
vmimglist = azurerm.list_vm_images_sub(access_token, subscription_id)
print(json.dumps(vmimglist, sort_keys=False, indent=2, separators=(',', ': ')))

for vm_image in vmimglist['value']:
    count += 1
    name = vm['name']
    location = vm['location']
    offer = vm['properties']['storageProfile']['imageReference']['offer']
    sku = vm['properties']['storageProfile']['imageReference']['sku']
    print(''.join([str(count), ': ', name,
                   # ', RG: ', rgname,
                   ', location: ', location,
                   ', OS: ', offer, ' ', sku]))



        
    
