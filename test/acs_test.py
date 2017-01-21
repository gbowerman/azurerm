# azurerm - unit tests - acs
# to run tests: python -m unittest acs_test.py

import sys
import unittest
from haikunator import Haikunator
import json
import azurerm
import time
import os

from os import chmod
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

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

        # create resource names
        h = Haikunator()
        self.rgname = h.haikunate()
        self.service_name = h.haikunate(delimiter='')
        self.agent_dns = h.haikunate(delimiter='')
        self.master_dns = h.haikunate(delimiter='')

        # generate RSA Key for container service
        key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, \
            key_size=2048)
        self.public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH, \
            serialization.PublicFormat.OpenSSH).decode('utf-8')
        
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

    def test_acs(self):
        # create container service
        agent_count = 3
        agent_vm_size = 'Standard_A1'
        master_count = 1
        admin_user = 'azure'
        print('Creating container service: ' + self.service_name)
        print('Agent DNS: ' + self.agent_dns)
        print('Master DNS: ' + self.master_dns)
        print('Agents: ' + str(agent_count) + ' * ' + agent_vm_size)
        print('Master count: ' + str(master_count))
        
        response = azurerm.create_container_service(self.access_token, self.subscription_id, \
            self.rgname, self.service_name, agent_count, agent_vm_size, self.agent_dns, \
            self.master_dns, admin_user, self.public_key, self.location, master_count=master_count)
        #print(json.dumps(response.json(), sort_keys=False, indent=2, separators=(',', ': ')))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], self.service_name)

        # get container service
        print('Getting container service: ' + self.service_name)
        response = azurerm.get_container_service(self.access_token, self.subscription_id, \
            self.rgname, self.service_name)
        self.assertEqual(response['name'], self.service_name)

        # list ACS operations
        print('Listing ACS operations')
        response = azurerm.list_acs_operations(self.access_token)
        self.assertTrue(len(response['value']) > 0)

        # list_container_services in resource group
        print('Listing container services in resource group')
        response = azurerm.list_container_services(self.access_token, self.subscription_id, self.rgname)
        self.assertTrue(len(response['value']) > 0)

        # list container services in subscription
        print('Listing container services in subscription')
        response = azurerm.list_container_services_sub(self.access_token, self.subscription_id)
        self.assertTrue(len(response['value']) > 0)

        # delete container service
        print('Deleting container service: ' + self.service_name)
        response = azurerm.delete_container_service(self.access_token, self.subscription_id, \
            self.rgname, self.service_name)
        self.assertEqual(response.status_code, 202)
        

if __name__ == '__main__':
    unittest.main()

