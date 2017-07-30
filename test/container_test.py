# azurerm - unit tests - container instances
# to run tests: python -m unittest container_test.py

import sys
import unittest
from haikunator import Haikunator
import json
import azurerm
import time
import os

from os import chmod

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
        #self.location = configData['location'] # comment out during preview
        self.location = 'westus'

        # create resource names
        h = Haikunator()
        self.rgname = h.haikunate()
        self.container_name = h.haikunate(delimiter='')
        
        # create resource group
        print('Creating resource group: ' + self.rgname)
        response = azurerm.create_resource_group(self.access_token, self.subscription_id, \
            self.rgname, self.location)
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        # delete resource group
        print('Deleting resource group: ' + self.rgname)
        response = azurerm.delete_resource_group(self.access_token, self.subscription_id, self.rgname)
        self.assertEqual(response.status_code, 202)

    def test_container(self):
        # create container instance
        container_port = 80
        image = 'nginx'
        print('Creating container instance: ' + self.container_name)
        
        response = azurerm.create_container_instance(self.access_token, self.subscription_id, \
            self.rgname, self.container_name, image, self.location, iptype = 'public', \
            port = container_port)
        # print(json.dumps(response.json(), sort_keys=False, indent=2, separators=(',', ': ')))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], self.container_name)

        # get container instance
        print('Getting container instance: ' + self.container_name)
        response = azurerm.get_container_instance(self.access_token, self.subscription_id, \
            self.rgname, self.container_name)
        self.assertEqual(response['name'], self.container_name)
        
        # list container instances in resource group
        print('Listing container instances in resource group')
        response = azurerm.list_container_instances(self.access_token, self.subscription_id, self.rgname)
        self.assertTrue(len(response['value']) > 0)

        # list container instances in subscription
        print('Listing container instances in subscription')
        response = azurerm.list_container_instances_sub(self.access_token, self.subscription_id)
        self.assertTrue(len(response['value']) > 0)

        # show container logs
        print('Getting container logs: ' + self.container_name)
        response = azurerm.get_container_logs(self.access_token, self.subscription_id, \
            self.rgname, self.container_name)
        #print(json.dumps(response, sort_keys=False, indent=2, separators=(',', ': ')))
        self.assertEqual(response['error']['code'], 'ContainerGroupTransitioning')

        # delete container instance
        print('Deleting container instance: ' + self.container_name)
        response = azurerm.delete_container_instance(self.access_token, self.subscription_id, \
            self.rgname, self.container_name)
        self.assertEqual(response.status_code, 200)
        

if __name__ == '__main__':
    unittest.main()

