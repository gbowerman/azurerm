'''azurerm unit tests - subscriptions and tenants'''
# to run tests: python -m unittest resource_groups_test.py

import sys
import unittest
import json

import azurerm


class TestAzurermPy(unittest.TestCase):

    def setUp(self):
        '''Load Azure app defaults'''
        try:
            with open('azurermconfig.json') as config_file:
                config_data = json.load(config_file)
        except FileNotFoundError:
            sys.exit("Error: Expecting azurermonfig.json in current folder")
        tenant_id = config_data['tenantId']
        app_id = config_data['appId']
        app_secret = config_data['appSecret']
        self.subscription_id = config_data['subscriptionId']
        self.access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    def tearDown(self):
        pass

    def test_subscriptions(self):
        # list subscriptions
        print('Listing subscriptions..')
        response = azurerm.list_subscriptions(self.access_token)
        # print(json.dumps(response, sort_keys=False, indent=2, separators=(',', ': ')))
        self.assertTrue(len(response['value']) > 0)

        # list locations
        print('Listing locations..')
        response = azurerm.list_locations(self.access_token, self.subscription_id)
        # print(json.dumps(response, sort_keys=False, indent=2, separators=(',', ': ')))
        self.assertTrue(len(response['value']) > 0)

        # list tenants
        print('Listing tenants..')
        response = azurerm.list_tenants(self.access_token)
        # print(json.dumps(response, sort_keys=False, indent=2, separators=(',', ': ')))
        self.assertTrue(len(response['value']) > 0)

if __name__ == '__main__':
    unittest.main()
