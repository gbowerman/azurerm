'''deploytemplatecli.py - deploys template URI and local params file, authenticates using CLI'''

import argparse
import json
import sys

import azurerm
from haikunator import Haikunator

def main():
    '''Main routine.'''
    # validate command line arguments
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--uri', '-u', required=True, action='store', help='Template URI')
    arg_parser.add_argument('--params', '-p', required=True, action='store',
                            help='Parameters json file')
    arg_parser.add_argument('--rg', '-g', required=True, action='store',
                            help='Resource Group name')
    arg_parser.add_argument('--sub', '-s', required=False, action='store',
                            help='subscription id (optional)')

    args = arg_parser.parse_args()

    template_uri = args.uri
    params = args.params
    rgname = args.rg
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


if __name__ == "__main__":
    main()
