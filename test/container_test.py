# azurerm - unit tests - container instances
# to run tests: python -m unittest container_test.py

import json
import os
import sys
import time
import unittest
from os import chmod

import azurerm
from haikunator import Haikunator


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
        self.access_token = azurerm.get_access_token(
            tenant_id, app_id, app_secret)
        # self.location = configData['location'] # comment out during preview
        self.location = 'westus'

        # create resource names
        h = Haikunator()
        self.rgname = h.haikunate()
        self.container_name = h.haikunate(delimiter='')
        self.container_name2 = h.haikunate(delimiter='')
        self.container_group_name = h.haikunate(delimiter='')

        # create resource group
        print('Creating resource group: ' + self.rgname)
        response = azurerm.create_resource_group(self.access_token, self.subscription_id,
                                                 self.rgname, self.location)
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        # delete resource group
        print('Deleting resource group: ' + self.rgname)
        response = azurerm.delete_resource_group(
            self.access_token, self.subscription_id, self.rgname)
        self.assertEqual(response.status_code, 202)

    def test_container(self):
        # create container instance group
        container_port = 80
        container_port2 = 81
        image = 'nginx'

        print('Creating container list..')
        container1_def = azurerm.create_container_definition(self.container_name, image, port=container_port)
        container2_def = azurerm.create_container_definition(self.container_name2, image, port=container_port2)
        container_list = [container1_def, container2_def]
        print('Creating container instance group: ' + self.container_group_name)

        response = azurerm.create_container_group(self.access_token, self.subscription_id,
                            self.rgname, self.container_group_name, container_list, self.location,
                            port=container_port, iptype='public')

        # print(json.dumps(response.json(), sort_keys=False, indent=2, separators=(',', ': ')))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], self.container_group_name)

        # get container group
        print('Getting container group: ' + self.container_group_name)
        response = azurerm.get_container_group(self.access_token, self.subscription_id,
                                               self.rgname, self.container_group_name)
        self.assertEqual(response['name'], self.container_group_name)

        # list container groups in resource group
        print('Listing container instance groups in resource group')
        response = azurerm.list_container_groups(
            self.access_token, self.subscription_id, self.rgname)
        self.assertTrue(len(response['value']) > 0)

        # list container groups in subscription
        print('Listing container instance groups in subscription')
        response = azurerm.list_container_groups_sub(
            self.access_token, self.subscription_id)
        self.assertTrue(len(response['value']) > 0)

        # show container logs
        print('Getting container logs: ' + self.container_group_name)
        response = azurerm.get_container_logs(self.access_token, self.subscription_id,
                                              self.rgname, self.container_group_name, container_name=self.container_name)
        #print(json.dumps(response, sort_keys=False, indent=2, separators=(',', ': ')))
        self.assertEqual(response['error']['code'],
                         'ContainerGroupTransitioning')

        # delete container group
        print('Deleting container instance: ' + self.container_name)
        response = azurerm.delete_container_group(self.access_token, self.subscription_id,
                                                  self.rgname, self.container_group_name)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
