# azurerm unit tests - network
# to run tests: python -m unittest storage_test.py

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
        self.rgname = Haikunator.haikunate()

        # create resource gorup
        print('Creating resource group: ' + self.rgname)
        response = azurerm.create_resource_group(self.access_token, self.subscription_id, \
            self.rgname, self.location)
        self.assertEqual(response.status_code, 201)

        # vnet name
        self.vnet = Haikunator.haikunate(delimiter='')
        self.ipname = self.vnet + 'ip'

    def tearDown(self):
        # delete resource group
        print('Deleting resource group: ' + self.rgname)
        response = azurerm.delete_resource_group(self.access_token, self.subscription_id, \
            self.rgname)
        self.assertEqual(response.status_code, 202)

    def test_network(self):
        # create public ip
        print('Creating public ip address: ' + self.ipname)
        dns_label = self.vnet
        response = azurerm.create_public_ip(self.access_token, self.subscription_id, self.rgname, \
            self.ipname, dns_label, self.location)
        self.assertEqual(response.status_code, 201)

        # create vnet
        print('Creating vnet: ' + self.vnet)
        response = azurerm.create_vnet(self.access_token, self.subscription_id, self.rgname, \
            self.vnet, self.location, address_prefix='10.0.0.0/16', nsg_id=None)
        self.assertEqual(response.status_code, 201)

        # get public ip
        print('Getting public ip ' + self.ipname)
        response = azurerm.get_public_ip(self.access_token, self.subscription_id, self.rgname, \
            self.ipname)
        self.assertEqual(response['name'], self.ipname)

        # get vnet
        print('Getting vnet: ' + self.vnet)
        response = azurerm.get_vnet(self.access_token, self.subscription_id, self.rgname, \
            self.vnet)
        self.assertEqual(response['name'], self.vnet)

        # delete public ip
        print('Deleting public ip ' + self.ipname)
        response = azurerm.delete_public_ip(self.access_token, self.subscription_id, self.rgname, \
            self.ipname)
        self.assertEqual(response.status_code, 202)

        # delete vnet
        print('Delete vnet: ' + self.vnet)
        response = azurerm.delete_vnet(self.access_token, self.subscription_id, self.rgname, \
            self.vnet)
        self.assertEqual(response.status_code, 202)


if __name__ == '__main__':
    unittest.main()

