import azurerm
import json

# Load Azure app defaults
try:
    with open('azurermconfig.json') as configFile:
        configData = json.load(configFile)
except FileNotFoundError:
    print("Error: Expecting azurermonfig.json in current folder")
    sys.exit()

tenant_id = configData['tenantId']
app_id = configData['appId']
app_secret = configData['appSecret']
subscription_id = configData['subscriptionId']
resource_group = configData['resourceGroup']
access_token = azurerm.get_access_token(
    tenant_id,
    app_id,
    app_secret
)

# create an availability set
print('Enter availability set name to create.')
asname = input()
location = 'eastus'
update_domains = 5
fault_domains = 3
asreturn = azurerm.create_as(access_token, subscription_id, resource_group, asname,
                             update_domains, fault_domains, location)
print(asreturn)

print('Availability set details...')

# get availability set details
as_info = azurerm.get_as(access_token, subscription_id, resource_group, asname)
print(json.dumps(as_info, sort_keys=False, indent=2, separators=(',', ': ')))