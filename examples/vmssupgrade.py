# Python script to upgrade a VM Scale Set one update domain at a time
# usage: vmssupgrade -r rgname -v vmssname -n newversion -u updatedomain [-y][--verbose][--nowait]
# test values for ubuntu 14.04 platform image:
#   oldversion = "14.04.201506100"
#   newversion = "14.04.201507060"
import argparse
import json
import sys
import time

import azurerm


def get_vm_ids_by_ud(access_token, subscription_id, resource_group, vmssname, updatedomain):
    instanceviewlist = azurerm.list_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmssname)
    # print(json.dumps(instanceviewlist, sort_keys=False, indent=2, separators=(',', ': ')))

    # loop through the instance view list, and build the vm id list of VMs in the matching UD
    udinstancelist = []
    for instanceView in instanceviewlist['value']:
        vmud = instanceView['properties']['instanceView']['platformUpdateDomain']
        if vmud == updatedomain:
            udinstancelist.append(instanceView['instanceId'])
    udinstancelist.sort()
    return udinstancelist


def main():
    # create parser
    argParser = argparse.ArgumentParser()

    argParser.add_argument('--vmssname', '-s', required=True, action='store', help='VM Scale Set name')
    argParser.add_argument('--resourcegroup', '-r', required=True, dest='resource_group', action='store',
                           help='Resource group name')
    argParser.add_argument('--newversion', '-n', dest='newversion', action='store',
                           help='New platform image version string')
    argParser.add_argument('--customuri', '-c', dest='customuri', action='store', help='New custom image URI string')
    argParser.add_argument('--updatedomain', '-u', dest='updatedomain', action='store', type=int,
                           help='Update domain (int)')
    argParser.add_argument('--vmid', '-i', dest='vmid', action='store', type=int, help='Single VM ID (int)')
    argParser.add_argument('--vmlist', '-l', dest='vmlist', action='store', help='List of VM IDs e.g. "["1", "2"]"')
    argParser.add_argument('--nowait', '-w', action='store_true', default=False,
                           help='Start upgrades and then exit without waiting')
    argParser.add_argument('--verbose', '-v', action='store_true', default=False, help='Show additional information')
    argParser.add_argument('-y', dest='noprompt', action='store_true', default=False,
                           help='Do not prompt for confirmation')

    args = argParser.parse_args()

    # switches to determine program behavior
    noprompt = args.noprompt  # go ahead and upgrade without waiting for confirmation when True
    nowait = args.nowait  # don't loop waiting for upgrade provisioning to complete when True
    verbose = args.verbose  # print extra status information when True

    vmssname = args.vmssname
    resource_group = args.resource_group
    if args.newversion is not None:
        newversion = args.newversion
        storagemode = 'platform'
    elif args.customuri is not None:
        customuri = args.customuri
        storagemode = 'custom'
    else:
        argParser.error('You must specify a new version for platform images or a custom uri for custom images')

    if args.updatedomain is not None:
        updatedomain = args.updatedomain
        upgrademode = 'updatedomain'
    elif args.vmid is not None:
        vmid = args.vmid
        upgrademode = 'vmid'
    elif args.vmlist is not None:
        vmlist = args.vmlist
        upgrademode = 'vmlist'
    else:
        argParser.error('You must specify an update domain, a vm id, or a vm list')

    # Load Azure app defaults
    try:
        with open('vmssconfig.json') as configFile:
            configdata = json.load(configFile)
    except FileNotFoundError:
        print("Error: Expecting vmssconfig.json in current folder")
        sys.exit()

    tenant_id = configdata['tenantId']
    app_id = configdata['appId']
    app_secret = configdata['appSecret']
    subscription_id = configdata['subscriptionId']

    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    # get the vmss model
    vmssmodel = azurerm.get_vmss(access_token, subscription_id, resource_group, vmssname)
    # print(json.dumps(vmssmodel, sort_keys=False, indent=2, separators=(',', ': ')))

    if storagemode == 'platform':
        # check current version
        imagereference = vmssmodel['properties']['virtualMachineProfile']['storageProfile']['imageReference']
        print('Current image reference in Scale Set model:')
        print(json.dumps(imagereference, sort_keys=False, indent=2, separators=(',', ': ')))

        # compare current version with new version
        if imagereference['version'] == newversion:
            print('Scale Set model version is already set to ' + newversion + ', skipping model update.')
        else:
            if not noprompt:
                response = input('Confirm version upgrade to: ' + newversion + ' (y/n)')
                if response.lower() != 'y':
                    sys.exit(1)
            # change the version
            vmssmodel['properties']['virtualMachineProfile']['storageProfile']['imageReference']['version'] = newversion
            # put the vmss model
            updateresult = azurerm.update_vmss(access_token, subscription_id, resource_group, vmssname,
                                               json.dumps(vmssmodel))
            if verbose:
                print(updateresult)
            print('OS version updated to ' + newversion + ' in model for VM Scale Set: ' + vmssname)
    else:  # storagemode = custom
        # check current uri
        oldimageuri = vmssmodel['properties']['virtualMachineProfile']['storageProfile']['osDisk']['image']['uri']
        print('Current image URI in Scale Set model:' + oldimageuri)

        # compare current uri with new uri
        if oldimageuri == customuri:
            print('Scale Set model version is already set to ' + customuri + ', skipping model update.')
        else:
            if not noprompt:
                response = input('Confirm uri upgrade to: ' + customuri + ' (y/n)')
                if response.lower() != 'y':
                    sys.exit(1)
            # change the version
            vmssmodel['properties']['virtualMachineProfile']['storageProfile']['osDisk']['image']['uri'] = customuri
            # put the vmss model
            updateresult = azurerm.update_vmss(access_token, subscription_id, resource_group, vmssname,
                                               json.dumps(vmssmodel))
            if verbose:
                print(updateresult)
            print('Image URI updated to ' + customuri + ' in model for VM Scale Set: ' + vmssname)

    # build the list of VMs to upgrade depending on the upgrademode setting
    if upgrademode == 'updatedomain':
        # list the VMSS VM instance views to determine their update domains
        print('Examining the scale set..')
        udinstancelist = get_vm_ids_by_ud(access_token, subscription_id, resource_group, vmssname, updatedomain)
        print('VM instances in UD: ' + str(updatedomain) + ' to upgrade:')
        print(udinstancelist)
        vmids = json.dumps(udinstancelist)
        print('Upgrading VMs in UD: ' + str(updatedomain))
    elif upgrademode == 'vmid':
        vmids = json.dumps([str(vmid)])
        print('Upgrading VM ID: ' + str(vmid))
    else:  # upgrademode = vmlist
        vmids = vmlist
        print('Upgrading VM IDs: ' + vmlist)

    # do manualupgrade on the VMs in the list
    upgraderesult = azurerm.upgrade_vmss_vms(access_token, subscription_id, resource_group, vmssname, vmids)
    print(upgraderesult)

    # now wait for upgrade to complete
    # query VM scale set instance view
    if not nowait:
        updatecomplete = False
        provisioningstate = ''
        while not updatecomplete:
            vmssinstanceview = azurerm.get_vmss_instance_view(access_token, subscription_id, resource_group, vmssname)
            for status in vmssinstanceview['statuses']:
                provisioningstate = status['code']
                if provisioningstate == 'ProvisioningState/succeeded':
                    updatecomplete = True
            if verbose:
                print(provisioningstate)
            time.sleep(5)
        print(status['code'])
    else:
        print('Check Scale Set provisioning state to determine when upgrade is complete.')


if __name__ == "__main__":
    main()
