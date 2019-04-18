#!/usr/bin/env python
''' deploytemplate.py - simple commandline deployment of a github template'''
# takes a deployment template URI and a local parameters file and deploys it
# requires an azurermconfig.json file containing service principal account to run

import argparse
import azurerm
from haikunator import Haikunator
import json
import time
import sys


def main():
    '''Main routine.'''
    # validate command line arguments
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--uri', '-u', required=True,
                           action='store', help='Template URI')
    argparser.add_argument('--params', '-f', required=True,
                           action='store', help='Parameters json file')
    argparser.add_argument('--location', '-l', required=True,
                           action='store', help='Location, e.g. eastus')
    argparser.add_argument('--rg', '-g', required=False,
                           action='store', help='Resource Group name')
    argparser.add_argument('--sub', '-s', required=False,
                           action='store', help='Subscription ID')
    argparser.add_argument('--genparams', '-p', required=False,
                           action='store', help='Comma separated list of parameters to generate strings for')
    argparser.add_argument('--wait', '-w', required=False, action='store_true', default=False,
                           help='Wait for deployment to complete and time it')
    argparser.add_argument('--debug', '-d', required=False, action='store_true', default=False,
                           help='Debug mode: print additional deployment')
    args = argparser.parse_args()

    template_uri = args.uri
    params = args.params
    rgname = args.rg
    location = args.location
    subscription_id = args.sub

    # Load Azure app defaults
    try:
        with open('azurermconfig.json') as configfile:
            configdata = json.load(configfile)
    except FileNotFoundError:
        sys.exit('Error: Expecting azurermconfig.json in current folder')

    tenant_id = configdata['tenantId']
    app_id = configdata['appId']
    app_secret = configdata['appSecret']
    if subscription_id is None:
        subscription_id = configdata['subscriptionId']

    # authenticate
    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    # load parameters file
    try:
        with open(params) as params_file:
            param_data = json.load(params_file)
    except FileNotFoundError:
        sys.exit('Error: Expecting ' + params + ' in current folder')

    # prep Haikunator
    haikunator = Haikunator()

    # if there is a genparams argument generate values and merge the list
    if args.genparams is not None:
        newdict = {}
        genlist = args.genparams.split(',')
        for param in genlist:
            # generate a random prhase, include caps and puncs in case it's a passwd
            newval = haikunator.haikunate(delimiter='-').title()
            newdict[param] = {'value': newval}
        params = {**param_data, **newdict}
    else:
        params = param_data


    # create resource group if not specified
    if rgname is None:
        rgname = haikunator.haikunate()
        ret = azurerm.create_resource_group(
            access_token, subscription_id, rgname, location)
        print('Creating resource group: ' + rgname +
              ', location:', location + ', return code:', ret)

    deployment_name = haikunator.haikunate()

    # measure time from beginning of deployment call (after creating resource group etc.)
    start_time = time.time()

    # deploy template and print response
    deploy_return = azurerm.deploy_template_uri(
        access_token, subscription_id, rgname, deployment_name, template_uri, params)
    print('Deployment name: ' + deployment_name +
          ', return code:', deploy_return)
    if 'Response [20' not in str(deploy_return):
        print('Return from deployment: ', deploy_return.text)
        sys.exit('Deployment failed. Exiting.. ')
    if args.debug is True:
        print(json.dumps(deploy_return.json(), sort_keys=False,
                         indent=2, separators=(',', ': ')))

    # show deployment status
    if args.debug is True:
        print('Deployment status:')
        deploy_return = azurerm.show_deployment(
            access_token, subscription_id, rgname, deployment_name)
        print(json.dumps(deploy_return, sort_keys=False,
                         indent=2, separators=(',', ': ')))
    
    # wait for deployment to complete
    if args.wait is True:
        print('Waiting for provisioning to complete..')
        provisioning_state = ''
        try:
            while True:
                time.sleep(10)
                deploy_return = azurerm.show_deployment(
                    access_token, subscription_id, rgname, deployment_name) 
                provisioning_state = deploy_return['properties']['provisioningState']
                if provisioning_state != 'Running':
                    break
            print('Provisioning state:', provisioning_state)
        except KeyError:
            print('Deployment failure:', deploy_return)

    elapsed_time = time.time() - start_time
    print('Elapsed time:', elapsed_time)
    
if __name__ == "__main__":
    main()
