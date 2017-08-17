'''create_rg.py - Create an Azure resource group'''
import json
import sys

import azurerm

# Load Azure app defaults
try:
    with open('azurermconfig.json') as config_file:
        CONFIG_DATA = json.load(config_file)
except FileNotFoundError:
    print("Error: Expecting azurermconfig.json in current folder")
    sys.exit()

TENANT_ID = CONFIG_DATA['tenantId']
APP_ID = CONFIG_DATA['appId']
APP_SECRET = CONFIG_DATA['appSecret']
SUB_ID = CONFIG_DATA['subscriptionId']

ACCESS_TOKEN = azurerm.get_access_token(TENANT_ID, APP_ID, APP_SECRET)

# create a resource group
print('Enter Resource group name to create.')
RGNAME = input()
LOCATION = 'eastus'
RET = azurerm.create_resource_group(ACCESS_TOKEN, SUB_ID, RGNAME, LOCATION)
print(RET)
