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
        # generate resource group name
        self.rgname = Haikunator.haikunate()

        # create resource gorup
        print('Creating resource group: ' + self.rgname)
        response = azurerm.create_resource_group(self.access_token, self.subscription_id, \
            self.rgname, self.location)
        self.assertEqual(response.status_code, 201)

        # create vnet
        self.vnet = Haikunator.haikunate(delimiter='')
        print('Creating vnet: ' + self.vnet)
        response = azurerm.create_vnet(self.access_token, self.subscription_id, self.rgname, \
            self.vnet, self.location, address_prefix='10.0.0.0/16', nsg_id=None)
        self.assertEqual(response.status_code, 201)
        self.subnet_id = response.json()['properties']['subnets'][0]['id']

        # create public ip address
        self.ipname = self.vnet + 'ip'
        print('Creating public ip address: ' + self.ipname)
        dns_label = self.vnet
        response = azurerm.create_public_ip(self.access_token, self.subscription_id, self.rgname, \
            self.ipname, dns_label, self.location)
        self.assertEqual(response.status_code, 201)
        self.ip_id = response.json()['id']

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

        # create nic
        nic_name = self.vnet + 'nic'
        print('Creating nic: ' + nic_name)
        response = azurerm.create_nic(self.access_token, self.subscription_id, self.rgname, \
            nic_name, self.ip_id, self.subnet_id, self.location)
        self.assertEqual(response.status_code, 201)
        self.nic_id = response.json()['id']

    def tearDown(self):
        # delete resource group - that deletes everything in the test
        print('Deleting resource group: ' + self.rgname)
        response = azurerm.delete_resource_group(self.access_token, self.subscription_id, \
            self.rgname)
        self.assertEqual(response.status_code, 202)

    def test_compute(self):

        # create VM
        
        # delete VM

        # get compute usage
        print('Getting compute usage')
        response = azurerm.get_compute_usage(self.access_token, self.subscription_id, self.location)
        self.assertTrue(len(response['value']) > 0)

if __name__ == '__main__':
    unittest.main()

