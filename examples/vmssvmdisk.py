'''vmssvmdisk.py - attach/detach disk to/from VMSS VM (preview functionality'''
import argparse
import json
import sys

import azurerm


def attach_model(subscription, rgname, vmssvm_model, diskname, lun):
    '''Attach a data disk to a VMSS VM model'''
    disk_id = '/subscriptions/' + subscription + '/resourceGroups/' + rgname + \
        '/providers/Microsoft.Compute/disks/' + diskname
    disk_model = {'lun': lun, 'createOption': 'Attach', 'caching': 'None',
                  'managedDisk': {'storageAccountType': 'Standard_LRS', 'id': disk_id}}
    vmssvm_model['properties']['storageProfile']['dataDisks'].append(disk_model)
    return vmssvm_model


def detach_model(vmssvm_model, lun):
    '''Detach a data disk from a VMSS VM model'''
    data_disks = vmssvm_model['properties']['storageProfile']['dataDisks']
    data_disks[:] = [disk for disk in data_disks if disk.get('lun') != lun]
    vmssvm_model['properties']['storageProfile']['dataDisks'] = data_disks
    return vmssvm_model


def main():
    '''Main routine.'''
    # validate command line arguments
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--vmssname', '-n', required=True, action='store',
                            help='Scale set name')
    arg_parser.add_argument('--rgname', '-g', required=True, action='store',
                            help='Resource Group Name')
    arg_parser.add_argument('--operation', '-o', required=True, action='store',
                            help='Operation (attach/detach)')
    arg_parser.add_argument('--vmid', '-i', required=True,
                            action='store', help='VM id')
    arg_parser.add_argument('--lun', '-l', required=True,
                            action='store', help='lun id')
    arg_parser.add_argument('--diskname', '-d', required=False, action='store',
                            help='Optional password')

    args = arg_parser.parse_args()
    vmssname = args.vmssname
    rgname = args.rgname
    operation = args.operation
    vmid = args.vmid
    lun = int(args.lun)
    diskname = args.diskname

    if operation != 'attach' and operation != 'detach':
        sys.exit('--operation must be attach or detach')
    if diskname is None and operation == 'attach':
        sys.exit('--diskname is required for attach operation.')

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

    # do a get on the VM
    vmssvm_model = azurerm.get_vmss_vm(access_token, subscription_id, rgname, vmssname, vmid)

    # check operation
    if operation == 'attach':
        new_model = attach_model(subscription_id, rgname, vmssvm_model, diskname, lun)
    else:
        if operation == 'detach':
            new_model = detach_model(vmssvm_model, lun)

    # do a put on the VM
    rmreturn = azurerm.put_vmss_vm(access_token, subscription_id, rgname, vmssname, vmid,
                                   new_model)

    if rmreturn.status_code != 201 and rmreturn.status_code != 202:
        sys.exit('Error ' + str(rmreturn.status_code) + ' creating VM. ' + rmreturn.text)

    print(json.dumps(rmreturn, sort_keys=False, indent=2, separators=(',', ': ')))

if __name__ == "__main__":
    main()
