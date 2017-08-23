# azurerm unit tests - Cosmos DB
# to run tests: python -m unittest cosmosdb_test.py

import sys
import unittest
from haikunator import Haikunator
import json
import azurerm

class TestAzurermPy(unittest.TestCase):

    def setUp(self):
        # Load Azure app defaults
        try:
            with open('azurermconfig.json') as configFile:
                configData = json.load(configFile)
        except FileNotFoundError:
            print("Error: Expecting azurermconfig.json in current folder")
            sys.exit()
        tenant_id = configData['tenantId']
        app_id = configData['appId']
        app_secret = configData['appSecret']
        self.subscription_id = configData['subscriptionId']
        self.access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)
        self.location = configData['location']
        h = Haikunator()
        self.rgname = h.haikunate()
        self.cosmosdbname = h.haikunate()

    def tearDown(self):
        pass

    def test_resource_groups(self):
        # create resource group
        print('Creating resource group: ' + self.rgname)
        response = azurerm.create_resource_group(self.access_token, self.subscription_id, \
            self.rgname, self.location)
        self.assertEqual(response.status_code, 201)

        # Create Cosmos DB account
        print('Creating Cosmos DB account: ' + self.cosmosdbname)

        response = azurerm.create_cosmosdb_account(self.access_token, self.subscription_id, self.rgname, \
            self.cosmosdbname, self.location, cosmosdb_kind='GlobalDocumentDB')
        self.assertEqual(response.status_code, 200)

        # delete resource group
        print('Deleting resource group: ' + self.rgname)
        response = azurerm.delete_resource_group(self.access_token, self.subscription_id, self.rgname)
        self.assertEqual(response.status_code, 202)

if __name__ == '__main__':
    unittest.main()