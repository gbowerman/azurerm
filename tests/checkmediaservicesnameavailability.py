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

# check media service name availability
name = "itisjustasimpletest"
response = azurerm.check_media_service_name_availability(access_token, subscription_id, name)
ms = response.json()
if (ms["NameAvailable"] == True):
	namestatus = "Available"
else:
	namestatus = "Unavailable"
print("MEDIA SERVICES CHECK FOR ACCOUNT NAME '" + name.upper() + "': " + namestatus)
