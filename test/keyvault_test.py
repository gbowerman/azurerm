'''azurerm - unit tests - keyvault''' 
# to run tests: python -m unittest keyvault_test.py

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
            with open('azurermconfig.json') as config_data:
                config_data = json.load(config_data)
        except FileNotFoundError:
            sys.exit("Error: Expecting azurermconfig.json in current folder")
        self.tenant_id = config_data['tenantId']
        self.app_id = config_data['appId']
        app_secret = config_data['appSecret']
        self.subscription_id = config_data['subscriptionId']
        self.access_token = azurerm.get_access_token(self.tenant_id, self.app_id, app_secret)
        self.location = config_data['location']
        h = Haikunator()
        self.rgname = h.haikunate()
        self.vault_name = h.haikunate()
        self.secret_name = h.haikunate()
        self.secret_value = h.haikunate()

        # create resource group
        print('Creating resource group: ' + self.rgname)
        response = azurerm.create_resource_group(self.access_token, self.subscription_id, \
            self.rgname, self.location)
        self.assertEqual(response.status_code, 201)


    def tearDown(self):
        # delete resource group
        print('Deleting resource group: ' + self.rgname)
        response = azurerm.delete_resource_group(self.access_token, self.subscription_id, 
                                                 self.rgname)
        self.assertEqual(response.status_code, 202)

    def test_keyvault(self):
        # create key vault
        print('Creating key vault: ' + self.vault_name)
        response = azurerm.create_keyvault(self.access_token, self.subscription_id, \
            self.rgname, self.vault_name, self.location, tenant_id=self.tenant_id, 
            object_id='64f8ea29-97c4-4bc9-a833-ceae2b3c7b42')
        # print(response.text)
        self.assertEqual(response.status_code, 200)

        # list keyvaults
        print('List key vaults')
        response = azurerm.list_keyvaults(self.access_token, self.subscription_id, self.rgname)
        # print(json.dumps(response, sort_keys=False, indent=2, separators=(',', ': ')))
        self.assertTrue('value' in response)

        # list keyvaults in subscription
        print('List key vaults in subscription')
        response = azurerm.list_keyvaults_sub(self.access_token, self.subscription_id)
        # print(json.dumps(response, sort_keys=False, indent=2, separators=(',', ': ')))
        self.assertTrue('value' in response)

        # get key vault status and wait for provisioning status to be Succeeded
        print('Get key vault and wait for successful provisioning..')
        provisioning_state = ''
        while provisioning_state != 'Succeeded':
            response = azurerm.get_keyvault(self.access_token, self.subscription_id, self.rgname, self.vault_name)
            # print(json.dumps(response, sort_keys=False, indent=2, separators=(',', ': ')))
            self.assertEqual(response['name'], self.vault_name)
            time.sleep(10)
            provisioning_state = response['properties']['provisioningState']
        vault_uri = response['properties']['vaultUri']

        # add a secret
        print('Adding secret ' + self.secret_name)
        response = azurerm.set_keyvault_secret(self.access_token, vault_uri, self.secret_name,
                                               self.secret_value)
        print(str(response.status_code))
        print(json.dumps(response.json))
        self.assertEqual(response.status_code, 200)

        # delete a secret
        print('Deleting secret ' + self.secret_name)
        response = azurerm.delete_keyvault_secret(self.access_token, vault_uri, self.secret_name)
        print(response.json())
        self.assertEqual(response.status_code, 200)

        # delete key vault
        print('Delete key vault: ' + self.vault_name)
        response = azurerm.delete_keyvault(self.access_token, self.subscription_id, \
            self.rgname, self.vault_name)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

