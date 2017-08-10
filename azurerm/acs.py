'''acs.py - azurerm functions for the Azure Container Service'''
import json
from .restfns import do_delete, do_get, do_put
from .settings import get_rm_endpoint, ACS_API


def create_container_service(access_token, subscription_id, resource_group, service_name, \
    agent_count, agent_vm_size, agent_dns, master_dns, admin_user, location, public_key=None,\
    master_count=3, orchestrator='DCOS', app_id=None, app_secret=None, admin_password=None, \
    ostype='Linux'):
    '''Create a new container service - include app_id and app_secret if using Kubernetes.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        service_name (str): Name of container service.
        agent_count (int): The number of agent VMs.
        agent_vm_size (str): VM size of agents, e.g. Standard_D1_v2.
        agent_dns (str): A unique DNS string for the agent DNS.
        master_dns (str): A unique string for the master DNS.
        admin_user (str): Admin user name.
        location (str): Azure data center location, e.g. westus.
        public_key (str): RSA public key (utf-8).
        master_count (int): Number of master VMs.
        orchestrator (str): Container orchestrator. E.g. DCOS, Kubernetes.
        app_id (str): Application ID for Kubernetes.
        app_secret (str): Application secret for Kubernetes.
        admin_password (str): Admin user password.
        ostype (str): Operating system. Windows of Linux.

    Returns:
        HTTP response. Container service JSON model.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerService/ContainerServices/', service_name,
                        '?api-version=', ACS_API])
    acs_body = {'location': location}
    properties = {'orchestratorProfile': {'orchestratorType': orchestrator}}
    properties['masterProfile'] = {'count': master_count, 'dnsPrefix': master_dns}
    ap_profile = {'name': 'AgentPool1'}
    ap_profile['count'] = agent_count
    ap_profile['vmSize'] = agent_vm_size
    ap_profile['dnsPrefix'] = agent_dns
    properties['agentPoolProfiles'] = [ap_profile]
    if ostype == 'Linux':
        linux_profile = {'adminUsername': admin_user}
        linux_profile['ssh'] = {'publicKeys': [{'keyData': public_key}]}
        properties['linuxProfile'] = linux_profile
    else: # Windows
        windows_profile = {'adminUsername': admin_user, 'adminPassword': admin_password}
        properties['windowsProfile'] = windows_profile
    if orchestrator == 'Kubernetes':
        sp_profile = {'ClientID': app_id}
        sp_profile['Secret'] = app_secret
        properties['servicePrincipalProfile'] = sp_profile
    acs_body['properties'] = properties
    body = json.dumps(acs_body)
    return do_put(endpoint, body, access_token)


def delete_container_service(access_token, subscription_id, resource_group, service_name):
    '''Delete a named container.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        service_name (str): Name of container service.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerService/ContainerServices/', service_name,
                        '?api-version=', ACS_API])
    return do_delete(endpoint, access_token)


def get_container_service(access_token, subscription_id, resource_group, service_name):
    '''Get details about an Azure Container Server

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        service_name (str): Name of container service.

    Returns:
        HTTP response. JSON model.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerService/ContainerServices/', service_name,
                        '?api-version=', ACS_API])
    return do_get(endpoint, access_token)


def list_acs_operations(access_token):
    '''List available Container Server operations.

        Args:
        access_token (str): A valid Azure authentication token.

    Returns:
        HTTP response. JSON model.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/providers/Microsoft.ContainerService/operations',
                        '?api-version=', ACS_API])
    return do_get(endpoint, access_token)


def list_container_services(access_token, subscription_id, resource_group):
    '''List the container services in a resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.

    Returns:
        HTTP response. JSON model.
   '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerService/ContainerServices',
                        '?api-version=', ACS_API])
    return do_get(endpoint, access_token)


def list_container_services_sub(access_token, subscription_id):
    '''List the container services in a subscription.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. JSON model.
   '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.ContainerService/ContainerServices',
                        '?api-version=', ACS_API])
    return do_get(endpoint, access_token)
