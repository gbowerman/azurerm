"""
Copyright (c) 2016, Marcelo Leal
Description: Simple Azure Resource Manager Python library
License: MIT (see LICENSE.txt file for details)
"""
import json
import azurerm

# Load Azure app defaults
try:
	with open('config.json') as configFile:
		configData = json.load(configFile)
except FileNotFoundError:
	print("ERROR: Expecting config.json in current folder")
	sys.exit()

tenant_id = configData['tenantId']
app_id = configData['appId']
app_secret = configData['appSecret']
subscription_id = configData['subscriptionId']
resourceGroup = configData['resourceGroup']
stoaccountName = configData['stoaccountName']
region = configData['region']

access_token = azurerm.get_access_token(
	tenant_id,
	app_id,
	app_secret
)

# list subscriptions
subscriptions = azurerm.list_subscriptions(access_token)
for sub in subscriptions["value"]:
	print("SUBSCRIPTION: " + sub["displayName"] + ': ' + sub["subscriptionId"])

# use the first subscription
subscription_id = subscriptions["value"][0]["subscriptionId"]

# create a media service account in a resource group
name = "itisjustasimpletest"
response = azurerm.create_media_service_rg(access_token, subscription_id, resourceGroup, region, stoaccountName, name)
if (response.status_code == 201):
	print("MEDIA SERVICE ACCOUNT: '" + name.upper() + "' CREATED OK.")
else:
	print("ERROR: Creating New MEDIA SERVICE ACCOUNT: " + name.upper())
