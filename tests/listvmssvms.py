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

access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)
resource_group = 'ah1'
vmssname = 'ah1'

instanceviewlist = azurerm.list_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmssname)
for vm in instanceviewlist['value']:
    ud = vm['properties']['instanceView']['platformUpdateDomain']
    fd = vm['properties']['instanceView']['platformFaultDomain']
    print('UD: ' + str(ud) + ', FD: ' + str(fd))
# print(json.dumps(instanceviewlist, sort_keys=False, indent=2, separators=(',', ': ')))
# vms = azurerm.list_vmss_vms(access_token, subscription_id, 'ah1', 'ah1')
# print(json.dumps(vms, sort_keys=False, indent=2, separators=(',', ': ')))
