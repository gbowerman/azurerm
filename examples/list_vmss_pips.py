'''list_vmss_pips.py - list a scale set public IP addresses'''
import argparse
import json
import re
import sys

import azurerm


def main():
    '''main reoutine'''
    # validate command line arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--vmssname', '-n', required=True,
                            action='store', help='VMSS Name')
    arg_parser.add_argument('--rgname', '-g', required=True,
                            action='store', help='Resource Group Name')
    arg_parser.add_argument('--details', '-a', required=False,
                            action='store', help='Print all details')
    args = arg_parser.parse_args()

    name = args.vmssname
    rgname = args.rgname
    details = args.details

    # Load Azure app defaults
    try:
        with open('azurermconfig.json') as config_file:
            config_data = json.load(config_file)
    except FileNotFoundError:
        print("Error: Expecting azurermconfig.json in current folder")
        sys.exit()
    tenant_id = config_data['tenantId']
    app_id = config_data['appId']
    app_secret = config_data['appSecret']
    subscription_id = config_data['subscriptionId']

    # authenticate
    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    # get public IPs
    public_ips = azurerm.get_vmss_public_ips(
        access_token, subscription_id, rgname, name)

    # print details
    if details is True:
        print(json.dumps(public_ips, sort_keys=False,
                         indent=2, separators=(',', ': ')))
    else:
        for pip in public_ips['value']:
            vm_id = re.search('Machines/(.*)/networkInt', pip['id']).group(1)
            ipaddr = pip['properties']['ipAddress']
            print('VM id: ' + vm_id + ', IP: ' + ipaddr)


if __name__ == "__main__":
    main()
