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

# app state variables
vmssProperties = []


def scale_event(scaleNum, access_token):
    global vmssProperties
    global rgname
    global vmssname
    global subscription_id
    newCapacity = vmssProperties[1] + scaleNum
    scaleoutput = azurerm.scale_vmss(access_token, subscription_id, rgname, vmssname, 'Standard_A1', 'Standard',
                                     newCapacity)
    print(scaleoutput)


access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

vmssget = azurerm.get_vmss(access_token, subscription_id, rgname, vmssname)
print(json.dumps(vmssget, sort_keys=False, indent=2, separators=(',', ': ')))
name = vmssget['name']
print('Name: ' + name)
location = vmssget['location']
print('Location: ' + location)
capacity = vmssget['sku']['capacity']
print('Capacity: ' + str(capacity))
offer = vmssget['properties']['virtualMachineProfile']['storageProfile']['imageReference']['offer']
print('Offer: ' + offer)
sku = vmssget['properties']['virtualMachineProfile']['storageProfile']['imageReference']['sku']
print('sku: ' + sku)
provisioningState = vmssget['properties']['provisioningState']
print('provisioning state: ' + provisioningState)
vmssProperties = [name, capacity, location, rgname, offer, sku, provisioningState]

scale_event(1, access_token)
