# deploytemplate.py
# authenticates using CLI e.g. run this in the Azure Cloud Shell
# takes a deployment template URI and a local parameters file and deploys it
# Arguments: -u templateUri
#            -p parameters JSON file
#            -l location
#            -g existing resource group
#            -s subscription
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
argParser.add_argument('--sub', '-s', required=False,
                       action='store', help='subscription id (optional)')                       

args = argParser.parse_args()

template_uri = args.uri
params = args.params
rgname = args.rg
location = args.location
subscription_id = args.sub

# load parameters file
try:
    with open(params) as params_file:
        param_data = json.load(params_file)
except FileNotFoundError:
    print('Error: Expecting ' + params + ' in current folder')
    sys.exit()

access_token = azurerm.get_access_token_from_cli()
if subscription_id is None:
    subscription_id = azurerm.get_subscription_from_cli()
deployment_name = Haikunator().haikunate() 
print('Deployment name:' + deployment_name)

deploy_return = azurerm.deploy_template_uri(
    access_token, subscription_id, rgname, deployment_name, template_uri, param_data)

print(json.dumps(deploy_return.json(), sort_keys=False, indent=2, separators=(',', ': ')))
