# VIP swap test script
# requires 2 load balancers, in the same resource group, with public IP addresses
# can be used to swap a staging scale application into production

import azurerm
import argparse
import json
import sys
from haikunator import Haikunator # used to create a random ip name for the floating ip
import time

def handle_bad_update(operation, ret):
    print("Error " + operation)
    print('Return code: ' + str(ret.status_code) + ' Error: ' + ret.text)
    sys.exit(1)


def main():
    # create parser
    argParser = argparse.ArgumentParser()

    # arguments: resource group lb name 1, 2
    argParser.add_argument('--resourcegroup', '-g', required=True, dest='resource_group', action='store', help='Resource group name')
    argParser.add_argument('--lb1', '-1', required=True, action='store', help='Load balancer 1 name')
    argParser.add_argument('--lb2', '-2', required=True, action='store', help='Load balancer 2 name')

    argParser.add_argument('--verbose', '-v', action='store_true', default=False, help='Show additional information')
    argParser.add_argument('-y', dest='noprompt', action='store_true', default=False, help='Do not prompt for confirmation')

    args = argParser.parse_args()

    verbose = args.verbose  # print extra status information when True

    resource_group = args.resource_group
    lb1 = args.lb1
    lb2 = args.lb2

    # Load Azure app defaults
    try:
        with open('azurermconfig.json') as configFile:
            configdata = json.load(configFile)
    except FileNotFoundError:
        print("Error: Expecting lbconfig.json in current folder")
        sys.exit()

    tenant_id = configdata['tenantId']
    app_id = configdata['appId']
    app_secret = configdata['appSecret']
    subscription_id = configdata['subscriptionId']

    access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    # figure out location of resource group and use that for the float ip
    rg = azurerm.get_resource_group(access_token, subscription_id, resource_group)
    location = rg['location']

    # Create a spare public IP address
    ip_name = Haikunator().haikunate(delimiter='')
    dns_label = ip_name + 'dns'
    print('Creating float public IP: ' + ip_name)
    ip_ret = azurerm.create_public_ip(access_token, subscription_id, resource_group, ip_name, dns_label, location)
    floatip_id = ip_ret.json()['id']
    if verbose is True:
        print('Float ip id = ' + floatip_id)
    
    # 1. Get lb 2
    lbmodel2 = azurerm.get_load_balancer(access_token, subscription_id, resource_group, lb2)
    lb2_ip_id = lbmodel2['properties']['frontendIPConfigurations'][0]['properties']['publicIPAddress']['id']
    lb2_ip_name = lb2_ip_id.split('publicIPAddresses/',1)[1] 
    if verbose is True:
        print(lb2 + ' ip id: ' + lb2_ip_id)
        print(lb2 + ' model:')
        print(json.dumps(lbmodel2, sort_keys=False, indent=2, separators=(',', ': ')))

    # 2. Assign new ip to lb 2
    print('Updating ' + lb2 + ' ip to float ip: ' + ip_name)
    lbmodel2['properties']['frontendIPConfigurations'][0]['properties']['publicIPAddress']['id'] = floatip_id
    ret = azurerm.update_load_balancer(access_token, subscription_id, resource_group, lb2, json.dumps(lbmodel2))
    if (ret.status_code != 200):
        handle_bad_update("updating " + lb2, ret)

    if verbose is True:
        print('original ip id: ' + lb2_ip_id + ', new ip id: ' + floatip_id)
        print(json.dumps(ret, sort_keys=False, indent=2, separators=(',', ': ')))
    print('Waiting for old ' + lb2 + ' ip: ' + lb2_ip_name + ' to be unnassigned')
    waiting = True
    start1 = time.time()
    while waiting:
        lbmodel2 = azurerm.get_load_balancer(access_token, subscription_id, resource_group, lb2)
        if lbmodel2['properties']['provisioningState'] == 'Succeeded':
            waiting = False
        time.sleep(3)
    end1 = time.time()
    print('Elapsed time: ' + str(int(end1 - start1)))
    # 3. Get lb 1
    lbmodel1 = azurerm.get_load_balancer(access_token, subscription_id, resource_group, lb1)
    lb1_ip_id = lbmodel1['properties']['frontendIPConfigurations'][0]['properties']['publicIPAddress']['id']

    if verbose is True:
        print(lb1 + ' ip id: ' + lb1_ip_id)
        print(lb1 + ' model:')
        print(json.dumps(lbmodel1, sort_keys=False, indent=2, separators=(',', ': ')))
    lb1_ip_name = lb1_ip_id.split('publicIPAddresses/',1)[1] 

    # 4. Assign old ip 2 to lb 1
    print('Downtime begins: Updating ' + lb1 + ' ip to ' + lb2_ip_name)
    start2 = time.time()
    lbmodel1['properties']['frontendIPConfigurations'][0]['properties']['publicIPAddress']['id'] = lb2_ip_id
    ret = azurerm.update_load_balancer(access_token, subscription_id, resource_group, lb1, json.dumps(lbmodel1))
    if (ret.status_code != 200):
        handle_bad_update("updating " + lb1, ret)
    if verbose is True:
        print(json.dumps(ret, sort_keys=False, indent=2, separators=(',', ': ')))

    print('Waiting for old ' + lb1 + ' ip: ' + lb1_ip_name + ' to be unnassigned')
    waiting = True
    while waiting:
        lbmodel1 = azurerm.get_load_balancer(access_token, subscription_id, resource_group, lb1)
        if lbmodel1['properties']['provisioningState'] == 'Succeeded':
            waiting = False
        time.sleep(3)
    end2 = time.time()
    print('Staging IP ' + lb2_ip_name + ' now points to old production LB ' + lb1)
    print('Elapsed time: ' + str(int(end2 - start1)))

    # 5. Assign old ip 1 to lb 2
    print('Updating ' + lb2 + ' ip to ' + lb1_ip_name)
    lbmodel2['properties']['frontendIPConfigurations'][0]['properties']['publicIPAddress']['id'] = lb1_ip_id
    ret = azurerm.update_load_balancer(access_token, subscription_id, resource_group, lb2, json.dumps(lbmodel2))
    if (ret.status_code != 200):
        handle_bad_update("updating " + lb2, ret)

    if verbose is True:
        print('Original ip id: ' + lb2_ip_id + ', new ip id: ' + lb1_ip_id)
        print(json.dumps(ret, sort_keys=False, indent=2, separators=(',', ': ')))
    print('Waiting for ' + lb2 + ' provisioning to complete')
    waiting = True
    while waiting:
        lbmodel2 = azurerm.get_load_balancer(access_token, subscription_id, resource_group, lb2)
        if lbmodel2['properties']['provisioningState'] == 'Succeeded':
            waiting = False
        time.sleep(3)
    end3 = time.time()

    # 6. Delete floatip
    print('VIP swap complete')
    print('Downtime: ' + str(int(end3 - start2)) + '. Total elapsed time: ' + \
        str(int(end3 - start1)))
    print('Deleting float ip: ' + ip_name)
    azurerm.delete_public_ip(access_token, subscription_id, resource_group, ip_name)

if __name__ == "__main__":
    main()