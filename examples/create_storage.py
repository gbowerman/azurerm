'''create_rg.py - example script to create an Azure resource group'''
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

print('Enter an existing Azure Resource Group name.')
RG_NAME = input()

# create a storage account
print('Enter storage account name to create.')
SA_NAME = input()
LOCATION = 'southeastasia'
RET = azurerm.create_storage_account(ACCESS_TOKEN, SUB_ID, RG_NAME, SA_NAME, LOCATION)
print(RET)

print('Storage account details...')

# get storage account details
SA_INFO = azurerm.get_storage_account(ACCESS_TOKEN, SUB_ID, RG_NAME, SA_NAME)
print(json.dumps(SA_INFO, sort_keys=False, indent=2, separators=(',', ': ')))

print('Storage account quota...')

# get storage account quota
QUOTA_INFO = azurerm.get_storage_usage(ACCESS_TOKEN, SUB_ID)
print(json.dumps(QUOTA_INFO, sort_keys=False, indent=2, separators=(',', ': ')))

print('Storage account keys...')

# get storage account keys
KEYS = azurerm.get_storage_account_keys(ACCESS_TOKEN, SUB_ID, RG_NAME, SA_NAME)
print(json.dumps(KEYS.text, sort_keys=False, indent=2, separators=(',', ': ')))
