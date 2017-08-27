'''jumpbox.py - creates a jumpbox VM in an existing VNET'''
import argparse
import json
import os
import sys
import time

import azurerm
from haikunator import Haikunator


def main():
    '''Main routine.'''
    # validate command line arguments
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--vmname', '-n', required=True, action='store', help='Name')
    arg_parser.add_argument('--rgname', '-g', required=True, action='store',
                            help='Resource Group Name')
    arg_parser.add_argument('--user', '-u', required=False, action='store', default='azure',
                            help='Optional username')
    arg_parser.add_argument('--password', '-p', required=False, action='store',
                            help='Optional password')
    arg_parser.add_argument('--sshkey', '-k', required=False, action='store',
                            help='SSH public key')
    arg_parser.add_argument('--sshpath', '-s', required=False, action='store',
                            help='SSH public key file path')
    arg_parser.add_argument('--location', '-l', required=False, action='store',
                            help='Location, e.g. eastus')
    arg_parser.add_argument('--vmsize', required=False, action='store', default='Standard_D1_V2',
                            help='VM size, defaults to Standard_D1_V2')
    arg_parser.add_argument('--dns', '-d', required=False, action='store',
                            help='DNS, e.g. myuniquename')
    arg_parser.add_argument('--vnet', required=False, action='store',
                            help='Optional VNET Name (else first VNET in resource group used)')
    arg_parser.add_argument('--nowait', action='store_true', default=False,
                            help='Do not wait for VM to finish provisioning')
    arg_parser.add_argument('--nonsg', action='store_true', default=False,
                            help='Do not create a network security group on the NIC')
    arg_parser.add_argument('--verbose', '-v', action='store_true', default=False,
                            help='Print operational details')

    args = arg_parser.parse_args()

    name = args.vmname
    rgname = args.rgname
    vnet = args.vnet
    location = args.location
    username = args.user
    password = args.password
    sshkey = args.sshkey
    sshpath = args.sshpath
    verbose = args.verbose
    dns_label = args.dns
    no_wait = args.nowait
    no_nsg = args.nonsg
    vmsize = args.vmsize

    # make sure all authentication scenarios are handled
    if sshkey is not None and sshpath is not None:
        sys.exit('Error: You can provide an SSH public key, or a public key file path, not both.')
    if password is not None and (sshkey is not None or sshpath is not None):
        sys.exit('Error: provide a password or SSH key (or nothing), not both')

    use_password = False
    if password is not None:
        use_password = True
    else:
        if sshkey is None and sshpath is None: # no auth parameters were provided
            # look for ~/id_rsa.pub
            home = os.path.expanduser('~')
            sshpath = home + os.sep + '.ssh' + os.sep + 'id_rsa.pub'
            if os.path.isfile(sshpath) is False:
                print('Default public key file not found.')
                use_password = True
                password = Haikunator().haikunate(delimiter=',') # creates random password
                print('Created new password = ' + password)
            else:
                print('Default public key file found')

    if use_password is False:
        print('Reading public key..')
        if sshkey is None:
            # at this point sshpath should have a valid Value
            with open(sshpath, 'r') as pub_ssh_file_fd:
                sshkey = pub_ssh_file_fd.read()

    # Load Azure app defaults
    try:
        with open('azurermconfig.json') as config_file:
            config_data = json.load(config_file)
    except FileNotFoundError:
        sys.exit("Error: Expecting azurermconfig.json in current folder")

    tenant_id = config_data['tenantId']
    app_id = config_data['appId']
    app_secret = config_data['appSecret']
    subscription_id = config_data['subscriptionId']

    # authenticate
    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    # if no location parameter was specified now would be a good time to figure out the location
    if location is None:
        try:
            rgroup = azurerm.get_resource_group(access_token, subscription_id, rgname)
            location = rgroup['location']
        except KeyError:
            print('Cannot find resource group ' + rgname + '. Check connection/authorization.')
            print(json.dumps(rgroup, sort_keys=False, indent=2, separators=(',', ': ')))
            sys.exit()
        print('location = ' + location)

    # get VNET
    print('Getting VNet')
    vnet_not_found = False
    if vnet is None:
        print('VNet not set, checking resource group')
        # get first VNET in resource group
        try:
            vnets = azurerm.list_vnets_rg(access_token, subscription_id, rgname)
            # print(json.dumps(vnets, sort_keys=False, indent=2, separators=(',', ': ')))
            vnetresource = vnets['value'][0]
        except IndexError:
            print('No VNET found in resource group.')
            vnet_not_found = True
            vnet = name + 'vnet'
    else:
        print('Getting VNet: ' + vnet)
        vnetresource = azurerm.get_vnet(access_token, subscription_id, rgname, vnet)
        if 'properties' not in vnetresource:
            print('VNet ' + vnet + ' not found in resource group ' + rgname)
            vnet_not_found = True

    if vnet_not_found is True:
        # create a vnet
        print('Creating vnet: ' + vnet)
        rmresource = azurerm.create_vnet(access_token, subscription_id, rgname, vnet, location, \
            address_prefix='10.0.0.0/16', nsg_id=None)
        if rmresource.status_code != 201:
            print('Error ' + str(vnetresource.status_code) + ' creating VNET. ' + vnetresource.text)
            sys.exit()
        vnetresource = azurerm.get_vnet(access_token, subscription_id, rgname, vnet)
    try:
        subnet_id = vnetresource['properties']['subnets'][0]['id']
    except KeyError:
        print('Subnet not found for VNet ' + vnet)
        sys.exit()
    if verbose is True:
        print('subnet_id = ' + subnet_id)

    public_ip_name = name + 'ip'
    if dns_label is None:
        dns_label = name + 'dns'

    print('Creating public ipaddr')
    rmreturn = azurerm.create_public_ip(access_token, subscription_id, rgname, public_ip_name,
                                        dns_label, location)
    if rmreturn.status_code not in [200, 201]:
        print(rmreturn.text)
        sys.exit('Error: ' + str(rmreturn.status_code) + ' from azurerm.create_public_ip()')
    ip_id = rmreturn.json()['id']
    if verbose is True:
        print('ip_id = ' + ip_id)

    print('Waiting for IP provisioning..')
    waiting = True
    while waiting:
        pip = azurerm.get_public_ip(access_token, subscription_id, rgname, public_ip_name)
        if pip['properties']['provisioningState'] == 'Succeeded':
            waiting = False
        time.sleep(1)

    if no_nsg is True:
        nsg_id = None
    else:
        # create NSG
        nsg_name = name + 'nsg'
        print('Creating NSG: ' + nsg_name)
        rmreturn = azurerm.create_nsg(access_token, subscription_id, rgname, nsg_name, location)
        if rmreturn.status_code not in [200, 201]:
            print('Error ' + str(rmreturn.status_code) + ' creating NSG. ' + rmreturn.text)
            sys.exit()
        nsg_id = rmreturn.json()['id']

        # create NSG rule for ssh, scp
        nsg_rule = 'ssh'
        print('Creating NSG rule: ' + nsg_rule)
        rmreturn = azurerm.create_nsg_rule(access_token, subscription_id, rgname, nsg_name,
                                           nsg_rule, description='ssh rule',
                                           destination_range='22')
        if rmreturn.status_code not in [200, 201]:
            print('Error ' + str(rmreturn.status_code) + ' creating NSG rule. ' + rmreturn.text)
            sys.exit()

    # create NIC
    nic_name = name + 'nic'
    print('Creating NIC: ' + nic_name)
    rmreturn = azurerm.create_nic(access_token, subscription_id, rgname, nic_name, ip_id,
                                  subnet_id, location, nsg_id=nsg_id)
    if rmreturn.status_code not in [200, 201]:
        print('Error ' + rmreturn.status_code + ' creating NSG rule. ' + rmreturn.text)
        sys.exit()
    nic_id = rmreturn.json()['id']

    print('Waiting for NIC provisioning..')
    waiting = True
    while waiting:
        nic = azurerm.get_nic(access_token, subscription_id, rgname, nic_name)
        if nic['properties']['provisioningState'] == 'Succeeded':
            waiting = False
        time.sleep(1)

    # create VM
    vm_name = name
    #publisher = 'CoreOS'
    #offer = 'CoreOS'
    #sku = 'Stable'
    publisher = 'Canonical'
    offer = 'UbuntuServer'
    sku = '16.04-LTS'
    version = 'latest'

    print('Creating VM: ' + vm_name)
    if use_password is True:
        rmreturn = azurerm.create_vm(access_token, subscription_id, rgname, vm_name, vmsize,
                                     publisher, offer, sku, version, nic_id, location,
                                     username=username, password=password)
    else:
        rmreturn = azurerm.create_vm(access_token, subscription_id, rgname, vm_name, vmsize,
                                     publisher, offer, sku, version, nic_id, location,
                                     username=username, public_key=sshkey)
    if rmreturn.status_code != 201:
        print('Error ' + rmreturn.status_code + ' creating VM. ' + rmreturn.text)
        sys.exit()
    if no_wait is False:
        print('Waiting for VM provisioning..')
        waiting = True
        while waiting:
            vm_model = azurerm.get_vm(access_token, subscription_id, rgname, vm_name)
            if vm_model['properties']['provisioningState'] == 'Succeeded':
                waiting = False
            time.sleep(5)
        print('VM provisioning complete.')
    print('Connect with:')
    print('ssh ' + dns_label + '.' + location + '.cloudapp.azure.com -l ' + username)

if __name__ == "__main__":
    main()
