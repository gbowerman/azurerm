#!/usr/bin/python
'''keyvault.py - creates and deletes Azure key vaults, using an MSI endpoint for authentication
   - This program must be run from an Azure Cloud Shell or a VM with MSI set up.
'''
import argparse
import os
import sys

import azurerm

def main():
    '''Main routine.'''
    # validate command line arguments
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--add', '-a', action='store_true', default=False,  help='add a key vault')
    arg_parser.add_argument('--delete', '-d', action='store_true', default=False,  help='delete a key vault')
    arg_parser.add_argument('--name', '-n', required=True, action='store', help='Name')
    arg_parser.add_argument('--rgname', '-g', required=True, action='store',
                            help='Resource Group Name')
    arg_parser.add_argument('--location', '-l', required=True, action='store',
                            help='Location, e.g. eastus')
    arg_parser.add_argument('--verbose', '-v', action='store_true', default=False,
                            help='Print operational details')

    args = arg_parser.parse_args()
    name = args.name
    rgname = args.rgname
    location = args.location

    if args.add is True and args.delete is True:
        sys.exit('Specify --add or --delete, not both.')
    if args.add is False and args.delete is False: 
        sys.exit('No operation specified, use --add or --delete.')

    if 'ACC_CLOUD' in os.environ and 'MSI_ENDPOINT' in os.environ:
        endpoint = os.environ['MSI_ENDPOINT']
    else:
        sys.exit('Not running in cloud shell or MSI_ENDPOINT not set') 

    # get Azure auth token
    if args.verbose is True:
        print('Getting Azure token from MSI endpoint..')

    access_token = azurerm.get_access_token_from_cli()

    if args.verbose is True:
        print('Getting Azure subscription ID from MSI endpoint..')
    subscription_id = azurerm.get_subscription_from_cli()

    # execute specified operation
    if  args.add is True: # create a key vault
        # get Azure tenant ID
        if args.verbose is True:
            print('Getting list of tenant IDs...')
        tenants = azurerm.list_tenants(access_token)
        tenant_id = tenants['value'][0]['tenantId']
        if args.verbose is True:
            print('My tenantId = ' + tenant_id)

        # get Graph object ID
        if args.verbose is True:
            print('Querying graph...')
        object_id = azurerm.get_object_id_from_graph()
        if args.verbose is True:
            print('My object ID = ' + object_id)

        # create key vault
        ret = azurerm.create_keyvault(access_token, subscription_id, rgname, name, location, tenant_id=tenant_id, object_id=object_id)
        if ret.status_code == 200:
            print('Successsfully created key vault: ' + name)
            print('Vault URI: ' + ret.json()['properties']['vaultUri'])
        else:
            print('Return code ' + str(ret.status_code) + ' from create_keyvault().')
            print(ret.text)

    # else delete named key vault
    else:
        ret = azurerm.delete_keyvault(access_token, subscription_id, rgname, name)
        if ret.status_code == 200:
            print('Successsfully deleted key vault: ' + name)
        else:
            print('Return code ' + str(ret.status_code) + ' from delete_keyvault().')
            print(ret.text)


if __name__ == '__main__':
    main()
