# azurerm - resource groups unit tests 
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

        # storage account name
        self.storage_account = Haikunator.haikunate(delimiter='')

    def tearDown(self):
        # delete resource group
        print('Deleting resource group: ' + self.rgname)
        response = azurerm.delete_resource_group(self.access_token, self.subscription_id, self.rgname)
        self.assertEqual(response.status_code, 202)

    def test_storage_accounts(self):

        # create storage account
        print('Creating storage account: ' + self.storage_account)
        response = azurerm.create_storage_account(self.access_token, self.subscription_id, \
            self.rgname, self.storage_account, self.location)
        self.assertEqual(response.status_code, 202)

        # get storage account
        print('Get storage account: ' + self.storage_account)
        response = azurerm.get_storage_account(self.access_token, self.subscription_id, \
            self.rgname, self.storage_account)
        self.assertEqual(response['name'], self.storage_account)

        # get storage account keys
        print('Get storage account keys')
        time.sleep(2) # small delay to allow account keys to be created
        response = azurerm.get_storage_account_keys(self.access_token, self.subscription_id, \
            self.rgname, self.storage_account) 
        keys = json.loads(response.text)
        self.assertTrue('keys' in keys)

        # get storage usage
        print('Get storage usage')
        response = azurerm.get_storage_usage(self.access_token, self.subscription_id)
        self.assertTrue('value' in response)

        # list storage accounts
        print('List storage accounts')
        response = azurerm.list_storage_accounts_rg(self.access_token, self.subscription_id, \
            self.rgname)
        self.assertTrue('value' in response)

        # list storage accounts in subscription
        print('List storage accounts in subscription')
        response = azurerm.list_storage_accounts_sub(self.access_token, self.subscription_id)
        self.assertTrue('value' in response)

        # delete storage account
        print('Delete storage account: ' + self.storage_account)
        response = azurerm.delete_storage_account(self.access_token, self.subscription_id, \
            self.rgname, self.storage_account)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

