# azurerm unit tests - compute
# To run tests: python -m unittest compute_test.py
# Note: The compute test unit has a more extensive setUp section than other units as the Compute
#  resources depend on storage and network resources. In fact running the Compute tests is a 
#  fairly good way to exercise storage, network AND compute functions.

import sys
import unittest
from haikunator import Haikunator
import json
import azurerm
import time
from random import choice
from string import ascii_lowercase


class TestAzurermPy(unittest.TestCase):

    def setUp(self):
        # Load Azure app defaults
        try:
            with open('azurermconfig.json') as configFile:
                configData = json.load(configFile)
        except FileNotFoundError:
            print("Error: Expecting vmssConfig.json in current folder")
            sys.exit()
        tenant_id = configData['tenantId']
        app_id = configData['appId']
        app_secret = configData['appSecret']
        self.subscription_id = configData['subscriptionId']
        self.access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)
        self.location = configData['location']
        
        # generate names used in tests
        self.rgname = Haikunator.haikunate()
        self.vnet = Haikunator.haikunate(delimiter='')
        self.saname = Haikunator.haikunate(delimiter='')
        self.vmname = Haikunator.haikunate(delimiter='')
        self.vmssname = Haikunator.haikunate(delimiter='')

        # create resource group
        print('Creating resource group: ' + self.rgname)
        response = azurerm.create_resource_group(self.access_token, self.subscription_id, \
            self.rgname, self.location)
        self.assertEqual(response.status_code, 201)

        # create vnet
        print('Creating vnet: ' + self.vnet)
        response = azurerm.create_vnet(self.access_token, self.subscription_id, self.rgname, \
            self.vnet, self.location, address_prefix='10.0.0.0/16', nsg_id=None)
        self.assertEqual(response.status_code, 201)
        self.subnet_id = response.json()['properties']['subnets'][0]['id']

        # create public ip address for VM NIC
        self.ipname = self.vnet + 'ip'
        print('Creating VM NIC public ip address: ' + self.ipname)
        dns_label = self.vnet
        response = azurerm.create_public_ip(self.access_token, self.subscription_id, self.rgname, \
            self.ipname, dns_label, self.location)
        self.assertEqual(response.status_code, 201)
        self.ip_id = response.json()['id']

        # create public ip address for VMSS LB
        self.ipname2 = self.vnet + 'ip2'
        print('Creating VMSS LB public ip address: ' + self.ipname2)
        dns_label2 = self.vnet + '2'
        response = azurerm.create_public_ip(self.access_token, self.subscription_id, self.rgname, \
            self.ipname2, dns_label2, self.location)
        self.assertEqual(response.status_code, 201)
        self.ip2_id = response.json()['id']

        # create storage account for VM 
        print('Creating storage account: ' + self.saname)
        response = azurerm.create_storage_account(self.access_token, self.subscription_id, self.rgname, \
            self.saname, self.location, storage_type='Standard_LRS')
        self.assertEqual(response.status_code, 202)

        # create 5 storage accounts for vmssname
        print('Creating storage accounts for scale set')
        self.container_list = []
        for count in range(5):
            sa_name = ''.join(choice(ascii_lowercase) for i in range(10))
            print(sa_name)
            response = azurerm.create_storage_account(self.access_token, self.subscription_id, \
                self.rgname, sa_name, self.location, storage_type='Standard_LRS')
            self.assertEqual(response.status_code, 202)
            container = 'https://' + sa_name + '.blob.core.windows.net/' + self.vmssname + 'vhd'
            self.container_list.append(container)

        # create NSG
        nsg_name = self.vnet + 'nsg'
        print('Creating NSG: ' + nsg_name)
        response = azurerm.create_nsg(self.access_token, self.subscription_id, self.rgname, \
            nsg_name, self.location)
        self.assertEqual(response.status_code, 201)
        # print(json.dumps(response.json()))
        self.nsg_id = response.json()['id']

        # create NSG rule
        nsg_rule = 'ssh'
        print('Creating NSG rule: ' + nsg_rule)
        response = azurerm.create_nsg_rule(self.access_token, self.subscription_id, self.rgname, \
            nsg_name, nsg_rule, description='ssh rule', destination_range='22')
        self.assertEqual(response.status_code, 201)

        # create nic for VM create
        nic_name = self.vnet + 'nic'
        print('Creating nic: ' + nic_name)
        response = azurerm.create_nic(self.access_token, self.subscription_id, self.rgname, \
            nic_name, self.ip_id, self.subnet_id, self.location)
        self.assertEqual(response.status_code, 201)
        self.nic_id = response.json()['id']

        # create load balancer with nat pool for VMSS create
        lb_name = self.vnet + 'lb'
        print('Creating load balancer with nat pool: ' + lb_name)
        response = azurerm.create_lb_with_nat_pool(self.access_token, self.subscription_id, \
            self.rgname, lb_name, self.ip2_id, '50000', '50100', '22', self.location)
        self.be_pool_id = response.json()['properties']['backendAddressPools'][0]['id']
        self.lb_pool_id = response.json()['properties']['inboundNatPools'][0]['id']

    def tearDown(self):
        # delete resource group - that deletes everything in the test
        print('Deleting resource group: ' + self.rgname)
        response = azurerm.delete_resource_group(self.access_token, self.subscription_id, \
            self.rgname)
        self.assertEqual(response.status_code, 202)

    def test_compute(self):
        # create VM
        vm_size = 'Standard_D1'
        publisher = 'Canonical'
        offer = 'UbuntuServer'
        sku = '16.04.0-LTS'
        version = 'latest'
        os_uri = 'http://' + self.saname + '.blob.core.windows.net/vhds/osdisk.vhd'
        username = 'rootuser'
        password = Haikunator.haikunate(delimiter=',')

        print('Creating VM: ' + self.vmname)
        response = azurerm.create_vm(self.access_token, self.subscription_id, self.rgname, \
            self.vmname, vm_size, publisher, offer, sku, version, self.saname, os_uri, \
            username, password, self.nic_id, self.location)
        # print(json.dumps(response.json()))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], self.vmname)

        # create VMSS
        capacity = 3
        print('Creating VMSS: ' + self.vmssname + ', capacity = ' + str(capacity))
        response = azurerm.create_vmss(self.access_token, self.subscription_id, self.rgname, \
            self.vmssname, vm_size, capacity, publisher, offer, sku, version, self.container_list, \
            username, password, self.subnet_id, self.be_pool_id, self.lb_pool_id, self.location)
        # print(json.dumps(response.json()))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], self.vmssname)

        # get compute usage
        print('Getting compute usage')
        response = azurerm.get_compute_usage(self.access_token, self.subscription_id, self.location)
        self.assertTrue(len(response['value']) > 0)

        # get vm instance view
        print('Getting VM instance view')
        response = azurerm.get_vm_instance_view(self.access_token, self.subscription_id, \
            self.rgname, self.vmname)
        # print(json.dumps(response, sort_keys=False, indent=2, separators=(',', ': ')))
        self.assertEqual(response['statuses'][0]['displayStatus'], 'Creating')

        # list vm instance views
        print('Listing VM instance views')
        response = azurerm.list_vm_instance_view(self.access_token, self.subscription_id, \
            self.rgname)
        # print(json.dumps(response, sort_keys=False, indent=2, separators=(',', ': ')))
        self.assertTrue(len(response['value']) > 0)

        # delete VM
        print('Deleting VM: ' + self.vmname)
        response = azurerm.delete_vm(self.access_token, self.subscription_id, self.rgname, \
            self.vmname)
        self.assertEqual(response.status_code, 202)

        # delete VMSS
        print('Deleting VMSS: ' + self.vmssname)
        response = azurerm.delete_vmss(self.access_token, self.subscription_id, self.rgname, \
            self.vmssname)
        self.assertEqual(response.status_code, 202)

if __name__ == '__main__':
    unittest.main()

