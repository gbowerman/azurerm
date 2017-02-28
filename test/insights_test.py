# azurerm unit tests - insights
# To run tests: python -m unittest insights_test.py
# Note: The insights test unit creates a VM scale set in order to add autoscale rules. 
# Therefore it is a fairly good way to exercise storage, network, compute AND insights functions.

import sys
import unittest
from haikunator import Haikunator
import json
import azurerm
import time
from random import choice
from string import ascii_lowercase


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
        
        # generate names for resources
        self.h = Haikunator()
        self.rgname = self.h.haikunate()
        self.vnet = self.h.haikunate(delimiter='')
        self.vmssname = self.h.haikunate(delimiter='')
        self.setting_name = self.h.haikunate(delimiter='')

        # create resource group
        print('Creating resource group: ' + self.rgname)
        response = azurerm.create_resource_group(self.access_token, self.subscription_id, \
            self.rgname, self.location)
        self.assertEqual(response.status_code, 201)

        # create vnet
        print('Creating vnet: ' + self.vnet)
        response = azurerm.create_vnet(self.access_token, self.subscription_id, self.rgname, \
            self.vnet, self.location, address_prefix='10.0.0.0/16', nsg_id=None)
        self.assertEqual(response.status_code, 201)
        self.subnet_id = response.json()['properties']['subnets'][0]['id']

        # create public ip address for VMSS LB
        self.ipname2 = self.vnet + 'ip2'
        print('Creating VMSS LB public ip address: ' + self.ipname2)
        dns_label2 = self.vnet + '2'
        response = azurerm.create_public_ip(self.access_token, self.subscription_id, self.rgname, \
            self.ipname2, dns_label2, self.location)
        self.assertEqual(response.status_code, 201)
        self.ip2_id = response.json()['id']

        # create load balancer with nat pool for VMSS create
        lb_name = self.vnet + 'lb'
        print('Creating load balancer with nat pool: ' + lb_name)
        response = azurerm.create_lb_with_nat_pool(self.access_token, self.subscription_id, \
            self.rgname, lb_name, self.ip2_id, '50000', '50100', '22', self.location)
        self.be_pool_id = response.json()['properties']['backendAddressPools'][0]['id']
        self.lb_pool_id = response.json()['properties']['inboundNatPools'][0]['id']

        # create VMSS
        capacity = 1
        vm_size = 'Standard_D1'
        publisher = 'Canonical'
        offer = 'UbuntuServer'
        sku = '16.04-LTS'
        version = 'latest'
        username = 'rootuser'
        password = self.h.haikunate(delimiter=',')
        print('Creating VMSS: ' + self.vmssname + ', capacity = ' + str(capacity))
        response = azurerm.create_vmss(self.access_token, self.subscription_id, self.rgname, \
            self.vmssname, vm_size, capacity, publisher, offer, sku, version, \
            self.subnet_id, self.be_pool_id, self.lb_pool_id, self.location, username=username, \
            public_key=self.public_key)
            

    def tearDown(self):
        # delete resource group - that deletes everything in the test
        print('Deleting resource group: ' + self.rgname)
        response = azurerm.delete_resource_group(self.access_token, self.subscription_id, \
            self.rgname)
        self.assertEqual(response.status_code, 202)


    def test_insights(self):
        # create autoscale rule
        print('Creating autoscale rules')
        metric_name = 'Percentage CPU'
        operator = 'GreaterThan'
        threshold = 60
        direction = 'Increase'
        change_count = 1
        rule1 = azurerm.create_autoscale_rule(self.subscription_id, self.rgname, self.vmssname, \
            metric_name, operator, threshold, direction, change_count)
        operator = 'LessThan'
        direction = 'Decrease'
        rule2 = azurerm.create_autoscale_rule(self.subscription_id, self.rgname, self.vmssname, \
            metric_name, operator, threshold, direction, change_count)
        rules = [rule1, rule2]
        # print(json.dumps(rules, sort_keys=False, indent=2, separators=(',', ': ')))

        # create autoscale setting
        print('Creating autoscale setting: ' + self.setting_name)
        min = 1
        max = 10
        default = 3
        response = azurerm.create_autoscale_setting(self.access_token, self.subscription_id, \
            self.rgname, self.setting_name, self.vmssname, self.location, min, max, default, \
            rules)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], self.setting_name)

if __name__ == '__main__':
    unittest.main()

