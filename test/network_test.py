# azurerm unit tests - network
# to run tests: python -m unittest network_test.py

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
        self.h = Haikunator()
        self.rgname = self.h.haikunate()

        # create resource group
        print('Creating resource group: ' + self.rgname)
        response = azurerm.create_resource_group(self.access_token, self.subscription_id, \
            self.rgname, self.location)
        self.assertEqual(response.status_code, 201)

        # generate vnet name
        self.vnet = self.h.haikunate(delimiter='')
        # generate public ip address names
        self.ipname = self.vnet + 'ip'
        self.lbipname = self.vnet + 'lbip'

    def tearDown(self):
        # delete resource group - that deletes everything in the test
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
        self.assertEqual(response.json()['name'], self.ipname)
        # print(json.dumps(response.json()))
        ip_id = response.json()['id']

        # create public ip for load balancer
        print('Creating public ip address for load balancer: ' + self.lbipname)
        dns_label = self.vnet + 'lb'
        response = azurerm.create_public_ip(self.access_token, self.subscription_id, self.rgname, \
            self.lbipname, dns_label, self.location)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], self.lbipname)
        # print(json.dumps(response.json()))
        lbip_id = response.json()['id']

        # create vnet
        print('Creating vnet: ' + self.vnet)
        response = azurerm.create_vnet(self.access_token, self.subscription_id, self.rgname, \
            self.vnet, self.location, address_prefix='10.0.0.0/16', nsg_id=None)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], self.vnet)
        subnet_id = response.json()['properties']['subnets'][0]['id']

        # create NSG
        nsg_name = self.vnet + 'nsg'
        print('Creating NSG: ' + nsg_name)
        response = azurerm.create_nsg(self.access_token, self.subscription_id, self.rgname, \
            nsg_name, self.location)
        self.assertEqual(response.status_code, 201)
        # print(json.dumps(response.json()))
        self.assertEqual(response.json()['name'], nsg_name)
        nsg_id = response.json()['id']

        # create NSG rule
        nsg_rule = 'ssh'
        print('Creating NSG rule: ' + nsg_rule)
        response = azurerm.create_nsg_rule(self.access_token, self.subscription_id, self.rgname, \
            nsg_name, nsg_rule, description='ssh rule', destination_range='22')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], nsg_rule)

        # create nic
        nic_name = self.vnet + 'nic'
        print('Creating nic: ' + nic_name)
        response = azurerm.create_nic(self.access_token, self.subscription_id, self.rgname, \
            nic_name, ip_id, subnet_id, self.location, nsg_id=nsg_id)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], nic_name)
        nic_id = response.json()['id']

        # create load balancer with nat pool
        lb_name = self.vnet + 'lb'
        print('Creating load balancer with nat pool: ' + lb_name)
        response = azurerm.create_lb_with_nat_pool(self.access_token, self.subscription_id, \
            self.rgname, lb_name, lbip_id, '50000', '50100', '22', self.location)
        # print(json.dumps(response.json()))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], lb_name)

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

        # list vnets
        print('Listing vnets in sub')
        response = azurerm.list_vnets(self.access_token, self.subscription_id)
        # print(json.dumps(response, sort_keys=False, indent=2, separators=(',', ': ')))
        self.assertTrue(len(response['value']) > 0)

        # get nic
        print('Getting nic: ' + nic_name)
        response = azurerm.get_nic(self.access_token, self.subscription_id, self.rgname, \
            nic_name)
        self.assertEqual(response['name'], nic_name)

        # list nics in resource group
        print('Listing nics in resource group: ' + self.rgname)
        response = azurerm.list_nics_rg(self.access_token, self.subscription_id, self.rgname)
        self.assertEqual(response['value'][0]['name'], nic_name)

        # list nics in subscription
        print('Listing nics in subscription.')
        response = azurerm.list_nics(self.access_token, self.subscription_id)
        self.assertTrue(len(response['value']) > 0)

        # delete nsg rule
        print('Deleting nsg rule: ' + nsg_rule)
        response = azurerm.delete_nsg_rule(self.access_token, self.subscription_id, self.rgname, \
            nsg_name, nsg_rule)
        self.assertEqual(response.status_code, 202)

        # delete nic
        print('Deleting nic: ' + nic_name)
        response = azurerm.delete_nic(self.access_token, self.subscription_id, self.rgname, \
            nic_name)
        self.assertEqual(response.status_code, 202)
        
        # delete nsg
        print('Deleting nsg: ' + nsg_name)
        response = azurerm.delete_nsg(self.access_token, self.subscription_id, self.rgname, \
            nsg_name)
        self.assertEqual(response.status_code, 202)

        # delete public ip
        print('Deleting public ip ' + self.ipname)
        response = azurerm.delete_public_ip(self.access_token, self.subscription_id, self.rgname, \
            self.ipname)
        self.assertEqual(response.status_code, 202)

        # delete load balancer
        print('Deleting load balancer ' + lb_name)
        response = azurerm.delete_load_balancer(self.access_token, self.subscription_id, self.rgname, \
            lb_name)
        self.assertEqual(response.status_code, 202)

        # delete vnet
        print('Deleting vnet: ' + self.vnet)
        response = azurerm.delete_vnet(self.access_token, self.subscription_id, self.rgname, \
            self.vnet)
        self.assertEqual(response.status_code, 202)

        # get network usage
        print('Getting network usage')
        response = azurerm.get_network_usage(self.access_token, self.subscription_id, self.location)
        self.assertTrue(len(response['value']) > 0)

if __name__ == '__main__':
    unittest.main()

