vm_name = 'myvm'
location = 'eastus'
vm_size = 'Standard_A1'
publisher = 'Canonical'
offer = 'UbuntuServer'
sku = '16.04.1-LTS'
os_type = 'linux'
version = 'latest'
storage_account = 'bugcraft2storage'
os_uri = 'http://' + storage_account + '.blob.core.windows.net/vhds/osdisk.vhd'
username = 'guybo'
password = 'mypassword'
nic_id = '/subscriptions/97ad66ae-0a22-4509-aeb4-8c84cf0f63ff/resourceGroups/gbrmtest4/providers/Microsoft.Network/networkInterfaces/gbrmtest4nic'

vm_size = 'Standard_A1'
publisher = 'Canonical'
offer = 'UbuntuServer'
sku = '16.04.1-LTS'
os_type = 'linux'
version = 'latest'
storage_account = 'bugcraft2storage'
os_uri = 'http://' + storage_account + '.blob.core.windows.net/vhds/osdisk.vhd'
username = 'guybo'
password = 'mypassword'
nic_id)

def create_vm(access_token, subscription_id, resource_group, vm_name, vm_size, publisher, offer, sku, os_type, version,
              storage_account, os_uri, username, password, nic_id, location):
    endpoint = ''.join([azure_rm_endpoint,
                    '/subscriptions/', subscription_id,
                    '/resourceGroups/', resource_group,
                    '/providers/Microsoft.Compute/virtualMachines/', name,
                    '?api-version=', COMP_API])
    body = ''.join(['{"name": "', vm_name,
                '","location": "', location,
                '","properties": { "hardwareProfile": {',
                '"vmSize": "', vm_size,
                '"},"storageProfile": { "imageReference": { "publisher": "', publisher,
                '","offer": "', offer,
                '","sku": "', sku,
                '","version": "', version,
                '"},"osDisk": { "osType": "', os_type,
                '", "name": "myosdisk1","vhd": {',
                '"uri": "', os_uri,
                '" }, "caching": "ReadWrite", "createOption": "fromImage" }},"osProfile": {',
                '"computerName": "', vm_name,
                '", "adminUsername": "', username,
                '", "adminPassword": "', password,
                '" }, "networkProfile": {',
                '"networkInterfaces": [{"id": "', nic_id,
                '", "properties": {"primary": true}}]}}}'])
    return do_put(endpoint, body, access_token)
print(body)