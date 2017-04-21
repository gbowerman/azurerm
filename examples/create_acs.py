import azurerm
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from haikunator import Haikunator  # used to generate random word strings
import json
import sys

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
sp_client_id = configData['servicePrincipalClientID']
sp_client_secret = configData['servicePrincipalClientSecret']

# authenticate
access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

location = 'eastus'

# create resource group
rgname = Haikunator.haikunate()
print('Creating resource group: ' + rgname)
response = azurerm.create_resource_group(access_token, subscription_id, rgname, location)
if response.status_code != 201:
    print(json.dumps(response.json(), sort_keys=False, indent=2, separators=(',', ': ')))
    sys.exit('Expecting return code 201 from create_resource_group(): ')

# create Container Service name and DNS values
service_name = Haikunator.haikunate(delimiter='')
agent_dns = Haikunator.haikunate(delimiter='')
master_dns = Haikunator.haikunate(delimiter='')

# generate RSA Key for container service
key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, \
    key_size=2048)
public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH, \
    serialization.PublicFormat.OpenSSH).decode('utf-8')

# create container service
agent_count = 3
agent_vm_size = 'Standard_A1'
master_count = 1
admin_user = 'azure'
print('Creating container service: ' + service_name)
print('Agent DNS: ' + agent_dns)
print('Master DNS: ' + master_dns)
print('Agents: ' + str(agent_count) + ' * ' + agent_vm_size)
print('Master count: ' + str(master_count))

response = azurerm.create_container_service(access_token, subscription_id, \
    rgname, service_name, agent_count, agent_vm_size, agent_dns, \
    master_dns, admin_user, public_key, location, app_id, \
    app_secret, master_count=master_count)
if response.status_code != 201:
    sys.exit('Expecting return code 201 from create_container_service(): ' + str(response.status_code))

print(json.dumps(response.json(), sort_keys=False, indent=2, separators=(',', ': ')))