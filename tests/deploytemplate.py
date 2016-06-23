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

location = 'Southeast Asia'

access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

template_uri = 'https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/201-vmss-lapstack-autoscale/azuredeploy.json'

raw_params = '{     "resourceLocation": {       "value": "LOCATION"     },     "vmSku": {       "value": "Standard_A1"     },     "ubuntuOSVersion": {       "value": "15.04"     },     "vmssName": {       "value": "VMSSNAME"     },     "instanceCount": {       "value": INSTANCECOUNT     },     "adminUsername": {       "value": "ADMINUSER"     },     "adminPassword": {       "value": "ADMINPASSWORD"     }   }'

print('Enter new resource group name')
rgname = input()

# create resource group
rgreturn = azurerm.create_resource_group(access_token, subscription_id, rgname, location)
print(rgreturn)

print('Enter VMSS name')
vmss_name = input()

print('Enter instance count')
instance_count = input()

params = raw_params.replace('VMSSNAME', vmss_name)
params = params.replace('INSTANCECOUNT', instance_count)
params = params.replace('LOCATION', location)

print('Enter user name')
user_name = input()

params = params.replace('ADMINUSER', user_name)

print('Enter password')
password = input()

params = params.replace('ADMINPASSWORD', password)

deploy_return = azurerm.deploy_template_uri(access_token, subscription_id, rgname, 'mydep3', template_uri, params)
print(deploy_return)
