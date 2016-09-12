import json

import azurerm

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
subscription_id = configData['subscriptionId']
resource_group = configData['resourceGroup']
vmssname = configData['vmssName']
location = 'westus'  # for quota API call

access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

# list VNETs in subscription
print('VNETs in subscription:')
vnets = azurerm.list_vnets(access_token, subscription_id)
for vnet in vnets['value']:
    print(vnet['name'] + ', ' + vnet['location'])

# list NICs in subscription
print('\nNICs in subscription:')
nics = azurerm.list_nics(access_token, subscription_id)
for nic in nics['value']:
    print(json.dumps(nic, sort_keys=False, indent=2, separators=(',', ': ')))
    # print(nic['name'])

# list nics in resource group
print('\nNICs in resource group: ' + resource_group)
nics = azurerm.list_nics_rg(access_token, subscription_id, resource_group)
for nic in nics['value']:
    print(json.dumps(nic, sort_keys=False, indent=2, separators=(',', ': ')))
    # print(nic['name'])

# list load balancers in subscription
print('\nLoad Balancers in subscription:')
lbs = azurerm.list_load_balancers(access_token, subscription_id)
for lb in lbs['value']:
    print(lb['name'] + ', ' + lb['location'])

# list load balancers in resource group
print('\nLoad Balancers in resource group: ' + resource_group)
lbs = azurerm.list_load_balancers_rg(access_token, subscription_id, resource_group)
for lb in lbs['value']:
    print(lb['name'] + ', ' + lb['location'])

# get details for a load balancer
lb_name = resource_group + 'lb'
print('\nLoad balancer ' + lb_name + ' details: ')
lb = azurerm.get_load_balancer(access_token, subscription_id, resource_group, lb_name)
# print(json.dumps(lb, sort_keys=False, indent=2, separators=(',', ': ')))

# list the public ip addresses in a resource group
print('\nPublic IPs in Resource Group ' + resource_group + ': ')
ips = azurerm.list_public_ips(access_token, subscription_id, resource_group)
# print(json.dumps(ips, sort_keys=False, indent=2, separators=(',', ': ')))

for ip in ips['value']:
    dns = ip['properties']['dnsSettings']['fqdn']
    if 'ipAddress' in ip['properties']:
        ipaddr = ip['properties']['ipAddress']
    else:
        ipaddr = 'no ip address'
    print(dns + ' (' + ipaddr + ')\n')

# get a public ip 
ip = azurerm.get_public_ip(access_token, subscription_id, resource_group, resource_group + 'pip')
print(json.dumps(ip, sort_keys=False, indent=2, separators=(',', ': ')))
dns = ip['properties']['dnsSettings']['fqdn']
if 'ipAddress' in ip['properties']:
    ipaddr = ip['properties']['ipAddress']
else:
    ipaddr = 'no ip address'
print(dns + ' (' + ipaddr + ')\n')

# get subscription limits by location
usage = azurerm.get_network_usage(access_token, subscription_id, location)
print('\nNetwork limits in ' + location + ':')
for property in usage['value']:
    print(property['name']['value'] + ': Current: '
          + str(property['currentValue']) + ', Limit: '
          + str(property['limit']))
