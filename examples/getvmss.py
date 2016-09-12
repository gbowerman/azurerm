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
rg = configData['resourceGroup']
vmss = configData['vmssName']

access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

print('Printing VMSS details\n')
vmssget = azurerm.get_vmss(access_token, subscription_id, rg, vmss)
name = vmssget['name']
capacity = vmssget['sku']['capacity']
location = vmssget['location']
offer = vmssget['properties']['virtualMachineProfile']['storageProfile']['imageReference']['offer']
sku = vmssget['properties']['virtualMachineProfile']['storageProfile']['imageReference']['sku']
print(json.dumps(vmssget, sort_keys=False, indent=2, separators=(',', ': ')))
print('Name: ' + name + ', capacity: ' + str(capacity) + ', ' + location + ', ' + offer + ', ' + sku)
print('\nPrinting VMSS instance view\n')
instanceView = azurerm.get_vmss_instance_view(access_token, subscription_id, rg, vmss)
print(json.dumps(instanceView, sort_keys=False, indent=2, separators=(',', ': ')))
'''
print('\nListing VMSS VMs\n')
vmss_vms = azurerm.list_vmss_vms(access_token, subscription_id, rg, vmss)
#print(vmss_vms)
print(json.dumps(vmss_vms, sort_keys=False, indent=2, separators=(',', ': ')))
for vm in vmss_vms['value']:
    instanceId = vm['instanceId']
    vmInstanceView = azurerm.get_vmss_vm_instance_view(access_token, subscription_id, rg, vmss, instanceId)
    print('\nVM ' + str(instanceId) + ' instance view\n')
    print(json.dumps(vmInstanceView, sort_keys=False, indent=2, separators=(',', ': ')))
 '''
