# acs.py - azurerm functions for Azure Container instances
import json
from .restfns import do_delete, do_get, do_put
from .settings import get_rm_endpoint, CONTAINER_API


# create_container_instance(access_token, subscription_id, resource_group, location, \
#    container_name, image, iptype='public', port=80, cpu=1.0, memgb=1.5, ostype='Linux')
# create a new container instance
def create_container_instance(access_token, subscription_id, resource_group, container_name, \
    image, location, iptype='public', port=80, cpu=1.0, memgb=1.5, ostype='Linux'):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups/', container_name,
                        '?api-version=', CONTAINER_API])
    container_body = {'location': location}
    properties = {'osType': ostype}
    container = {'name': container_name}
    container_properties = {'image': image}
    container_properties['ports'] = [{'port': port}]
    container_properties['resources'] = {'requests': {'cpu': cpu, 'memoryInGB': memgb}}
    container['properties'] = container_properties
    properties['containers'] = [container]
    ipport = {'protocol': 'TCP'}
    ipport['port'] = port
    ipaddress = {'ports': [ipport]}
    ipaddress['type'] = iptype
    properties['ipAddress'] = ipaddress
    container_body['properties'] = properties

    body = json.dumps(container_body)
    return do_put(endpoint, body, access_token)


# delete_container_instance(access_token, subscription_id, resource_group, container_name)
# delete a named container instance
def delete_container_instance(access_token, subscription_id, resource_group, container_name):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups/', container_name,
                        '?api-version=', CONTAINER_API])
    return do_delete(endpoint, access_token)


# get_container_instance(access_token, subscription_id, resource_group, container_name)
# get details about a container instance
def get_container_instance(access_token, subscription_id, resource_group, container_name):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups/', container_name,
                        '?api-version=', CONTAINER_API])
    return do_get(endpoint, access_token)


# list_container_instances_sub(access_token, subscription_id)
# list all container instances in a subscription
def get_container_logs(access_token, subscription_id, resource_group, container_name):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups/', container_name,
                        '/containers/', container_name, '/logs?api-version=', CONTAINER_API])
    return do_get(endpoint, access_token)


# list_container_instances(access_token, subscription_id, resource_group)
# list container instances in a resource group
def list_container_instances(access_token, subscription_id, resource_group):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups', 
                        '?api-version=', CONTAINER_API])
    return do_get(endpoint, access_token)


# list_container_instances_sub(access_token, subscription_id)
# list all container instances in a subscription
def list_container_instances_sub(access_token, subscription_id):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups', 
                        '?api-version=', CONTAINER_API])
    return do_get(endpoint, access_token)