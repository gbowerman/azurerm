# acs.py - azurerm functions for the Azure Container Service
import json
from .restfns import do_delete, do_get, do_put
from .settings import azure_rm_endpoint, ACS_API


# create_container_service(access_token, subscription_id, resource_group, service_name, \
#    agent_count, agent_vm_size, agent_dns, master_dns, admin_user, public_key, location, \
#    master_count=3, orchestrator='DCOS')
# create a new container service
def create_container_service(access_token, subscription_id, resource_group, service_name, \
    agent_count, agent_vm_size, agent_dns, master_dns, admin_user, public_key, location, \
    app_id, app_secret, master_count=3, orchestrator='DCOS'):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerService/ContainerServices/', service_name,
                        '?api-version=', ACS_API])
    acs_body = {'location': location }
    properties = {'orchestratorProfile': { 'orchestratorType': orchestrator}}
    properties['masterProfile'] = {'count': master_count, 'dnsPrefix': master_dns}
    ap_profile = {'name': 'AgentPool1'}
    ap_profile['count'] = agent_count
    ap_profile['vmSize'] = agent_vm_size
    ap_profile['dnsPrefix'] = agent_dns
    properties['agentPoolProfiles'] = [ap_profile]
    linux_profile = {'adminUsername': admin_user}
    linux_profile['ssh'] = {'publicKeys': [{'keyData': public_key}]}
    properties['linuxProfile'] = linux_profile
    sp_profile = {'ClientID': app_id}
    sp_profile['Secret'] = app_secret
    properties['servicePrincipalProfile'] = sp_profile
    acs_body['properties'] = properties
    body = json.dumps(acs_body)
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
