# deploytemplate.py
# takes a deployment template URI and a local parameters file and deploys it
# Arguments: --uri templateUri
#            --params parameters JSON file
#            -l location
#            -g existing resource group
import argparse
import azurerm
from haikunator import Haikunator
import json
import sys

# validate command line arguments
argParser = argparse.ArgumentParser()

argParser.add_argument('--uri', '-u', required=True,
                       action='store', help='Template URI')
argParser.add_argument('--params', '-p', required=True,
                       action='store', help='Parameters json file')
argParser.add_argument('--location', '-l', required=True,
                       action='store', help='Location, e.g. eastus')
argParser.add_argument('--rg', '-g', required=True,
                       action='store', help='Resource Group name')

args = argParser.parse_args()

template_uri = args.uri
params = args.params
rgname = args.rg
location = args.location

# Load Azure app defaults
try:
    with open('azurermconfig.json') as config_file:
        config_data = json.load(config_file)
except FileNotFoundError:
    print('Error: Expecting azurermconfig.json in current folder')
    sys.exit()

tenant_id = config_data['tenantId']
app_id = config_data['appId']
app_secret = config_data['appSecret']
subscription_id = config_data['subscriptionId']

# load parameters file
try:
    with open(params) as params_file:
        param_data = json.load(params_file)
except FileNotFoundError:
    print('Error: Expecting ' + params + ' in current folder')
    sys.exit()

access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)
deployment_name = Haikunator().haikunate() 
print('Deployment name:' + deployment_name)

deploy_return = azurerm.deploy_template_uri(
    access_token, subscription_id, rgname, deployment_name, template_uri, json.dumps(param_data))
print(deploy_return)
