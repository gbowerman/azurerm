'''create_as.py - create an Azure Availability Set'''
import json
import sys

import azurerm

# Load Azure app defaults
try:
    with open('azurermconfig.json') as configFile:
        CONFIG_DATA = json.load(configFile)
except FileNotFoundError:
    print("Error: Expecting azurermonfig.json in current folder")
    sys.exit()

TENANT_ID = CONFIG_DATA['tenantId']
APP_ID = CONFIG_DATA['appId']
APP_SECRET = CONFIG_DATA['appSecret']
SUB_ID = CONFIG_DATA['subscriptionId']
LOCATION = CONFIG_DATA['region']
ACCESS_TOKEN = azurerm.get_access_token(TENANT_ID, APP_ID, APP_SECRET)

print('Enter an existing Azure Resource Group name.')
RG_NAME = input()

# create an availability set
print('Enter availability set name to create.')
AS_NAME = input()
UDS = 5
FDS = 3
RET = azurerm.create_as(ACCESS_TOKEN, SUB_ID, RG_NAME, AS_NAME, UDS, FDS, LOCATION)
print(RET)

# get availability set details
print('Availability set details...')
AS_INFO = azurerm.get_as(ACCESS_TOKEN, SUB_ID, RG_NAME, AS_NAME)
print(json.dumps(AS_INFO, sort_keys=False, indent=2, separators=(',', ': ')))
