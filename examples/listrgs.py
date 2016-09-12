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

access_token = azurerm.get_access_token(
    tenant_id,
    app_id,
    app_secret
)

# list resource groups
resource_groups = azurerm.list_resource_groups(access_token, subscription_id)
for rg in resource_groups["value"]:
    print(rg["name"] + ', ' + rg["location"] + ', ' + rg["properties"]["provisioningState"])
