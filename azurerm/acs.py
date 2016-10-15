# acs.py - azurerm functions for the Azure Container Service

from .restfns import do_delete, do_get, do_put
from .settings import azure_rm_endpoint, ACS_API


# create_container_service(access_token, subscription_id, resource_group, service_name, \
#    agent_count, agent_vm_size, agent_dns, master_dns, admin_user, public_key, location, \
#    master_count=3, orchestrator='DCOS')
# create a new container service 
def create_container_service(access_token, subscription_id, resource_group, service_name, \
    agent_count, agent_vm_size, agent_dns, master_dns, admin_user, public_key, location, \
    master_count=3, orchestrator='DCOS'):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerService/ContainerServices/', service_name,
                        '?api-version=', ACS_API])
    body = ''.join(['{  "location": "', location, 
        '", "properties": { "orchestratorProfile": { "orchestratorType": "', orchestrator,
        '" }, "masterProfile": { "count": ', str(master_count),
        ', "dnsPrefix": "', master_dns, 
        '"}, "agentPoolProfiles": [ { "name": "AgentPool1", "count": ', str(agent_count),
        ', "vmSize": "', agent_vm_size,
        '", "dnsPrefix": "', agent_dns, 
        '"}],"linuxProfile": {"adminUsername": "', admin_user,
        '","ssh": {"publicKeys": [{"keyData": "', public_key,
        '"}]}}}}'])
    return do_put(endpoint, body, access_token)

# delete_container_service(access_token, subscription_id, resource_group, container_service_name) 
# delete a named container service
def delete_container_service(access_token, subscription_id, resource_group, service_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerService/ContainerServices/', service_name,
                        '?api-version=', ACS_API])
    return do_delete(endpoint, access_token)


# get_container_service(access_token, subscription_id, resource_group, service_name)
# get details about an Azure Container Server
def get_container_service(access_token, subscription_id, resource_group, service_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerService/ContainerServices/', service_name,
                        '?api-version=', ACS_API])
    return do_get(endpoint, access_token)    


# list_acs_operations(access_token, subscription_id, resource_group)
# list available Container Server operations
def list_acs_operations(access_token):
    endpoint = ''.join([azure_rm_endpoint,
                        '/providers/Microsoft.ContainerService/operations',
                        '?api-version=', ACS_API])
    return do_get(endpoint, access_token)


# list_container_services(access_token, subscription_id, resource_grou)
# list the container services in a resource group
def list_container_services(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerService/ContainerServices',
                        '?api-version=', ACS_API])
    return do_get(endpoint, access_token)  


# list_container_services_sub(access_token, subscription_id)
# list the container services in a subscription
def list_container_services_sub(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.ContainerService/ContainerServices',
                        '?api-version=', ACS_API])
    return do_get(endpoint, access_token)

