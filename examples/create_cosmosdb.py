'''create_cosmosdb.py - example script to create an Cosmos DB account'''
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

# create a Cosmos DB account
print('Enter Cosmos DB account name to create.')
CA_NAME = input()
LOCATION = 'eastus'
RET = azurerm.create_cosmosdb_account(ACCESS_TOKEN, SUB_ID, RG_NAME, CA_NAME, LOCATION, cosmosdb_kind='GlobalDocumentDB')
print(RET)

print('It can take 2-3 minutes to create the Cosmos DB account. The example below is for reference. This likely falls if ran right away.')

# get storage account keys
KEYS = azurerm.get_cosmosdb_account_keys(ACCESS_TOKEN, SUB_ID, RG_NAME, CA_NAME)
print(json.dumps(KEYS.text, sort_keys=False, indent=2, separators=(',', ': ')))
