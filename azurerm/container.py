# acs.py - azurerm functions for Azure Container instances
import json
from .restfns import do_delete, do_get, do_put
from .settings import get_rm_endpoint, CONTAINER_API


# create_container_definition(container_name, image, port=80, cpu=1.0, memgb=1.5, environment=None)
# makes a python dictionary of container properties - make a list of these to pass to 
# create_container_group()
def create_container_definition(container_name, image, port=80, cpu=1.0, memgb=1.5, environment=None):
    container = {'name': container_name}
    container_properties = {'image': image}
    container_properties['ports'] = [{'port': port}]
    container_properties['resources'] = {
        'requests': {'cpu': cpu, 'memoryInGB': memgb}}
    container['properties'] = container_properties
    # environment param must be a list of [{'name':'envname', 'value':'envvalue'}]
    if environment is not None:
        container_properties['environmentVariables'] = environment
    return container


# create_container_group(access_token, subscription_id, resource_group, container_group_name,
#    container_list, location, ostype='Linux', port=80, iptype='public')
# create a new container instance - implicitly creates a container group
def create_container_group(access_token, subscription_id, resource_group, container_group_name,
                              container_list, location, ostype='Linux', port=80, iptype='public'):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups/', container_group_name,
                        '?api-version=', CONTAINER_API])
    container_group_body = {'location': location}
    properties = {'osType': ostype}
    properties['containers'] = container_list
    ipport = {'protocol': 'TCP'}
    ipport['port'] = port
    ipaddress = {'ports': [ipport]}
    ipaddress['type'] = iptype
    properties['ipAddress'] = ipaddress
    container_group_body['properties'] = properties
    body = json.dumps(container_group_body)
    return do_put(endpoint, body, access_token)


# delete_container_group(access_token, subscription_id, resource_group, container_name)
# delete a named container instance
def delete_container_group(access_token, subscription_id, resource_group, container_group_name):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups/', container_group_name,
                        '?api-version=', CONTAINER_API])
    return do_delete(endpoint, access_token)


# get_container_group(access_token, subscription_id, resource_group, container_name)
# get details about a container instance
def get_container_group(access_token, subscription_id, resource_group, container_group_name):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups/', container_group_name,
                        '?api-version=', CONTAINER_API])
    return do_get(endpoint, access_token)


# get_container_logs(access_token, subscription_id, resource_group, container_name
# show the container logs
def get_container_logs(access_token, subscription_id, resource_group, container_group_name, container_name=None):
    if container_name is None:
        container_name = container_group_name
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups/', container_group_name,
                        '/containers/', container_name, '/logs?api-version=', CONTAINER_API])
    return do_get(endpoint, access_token)


# list_container_groups(access_token, subscription_id, resource_group)
# list container groups in a resource group
def list_container_groups(access_token, subscription_id, resource_group):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups',
                        '?api-version=', CONTAINER_API])
    return do_get(endpoint, access_token)


# list_container_groups_sub(access_token, subscription_id)
# list all container groups in a subscription
def list_container_groups_sub(access_token, subscription_id):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups',
                        '?api-version=', CONTAINER_API])
    return do_get(endpoint, access_token)