''' container.py - azurerm functions for Azure Container instances'''
import json
from .restfns import do_delete, do_get, do_put
from .settings import get_rm_endpoint, CONTAINER_API


def create_container_definition(container_name, image, port=80, cpu=1.0, memgb=1.5,
                                environment=None):
    '''Makes a python dictionary of container properties.

    Args:
        container_name: The name of the container.
        image (str): Container image string. E.g. nginx.
        port (int): TCP port number. E.g. 8080.
        cpu (float): Amount of CPU to allocate to container. E.g. 1.0.
        memgb (float): Memory in GB to allocate to container. E.g. 1.5.
        environment (list): A list of [{'name':'envname', 'value':'envvalue'}].
        Sets environment variables in the container.

    Returns:
        A Python dictionary of container properties, pass a list of these to
        create_container_group().
    '''
    container = {'name': container_name}
    container_properties = {'image': image}
    container_properties['ports'] = [{'port': port}]
    container_properties['resources'] = {
        'requests': {'cpu': cpu, 'memoryInGB': memgb}}
    container['properties'] = container_properties

    if environment is not None:
        container_properties['environmentVariables'] = environment
    return container


def create_container_instance_group(access_token, subscription_id, resource_group,
                                    container_group_name, container_list, location,
                                    ostype='Linux', port=80, iptype='public'):
    '''Create a new container group with a list of containers specifified by container_list.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        container_group_name (str): Name of container instance group.
        container_list (list): A list of container properties. Use create_container_definition to
        create each container property set.
        location (str): Azure data center location. E.g. westus.
        ostype (str): Container operating system type. Linux or Windows.
        port (int): TCP port number. E.g. 8080.
        iptype (str): Type of IP address. E.g. public.

    Returns:
        HTTP response with JSON body of container group.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups/',
                        container_group_name,
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


def delete_container_instance_group(access_token, subscription_id, resource_group,
                                    container_group_name):
    '''Delete a container group from a resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        container_group_name (str): Name of container instance group.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups/',
                        container_group_name,
                        '?api-version=', CONTAINER_API])
    return do_delete(endpoint, access_token)


def get_container_instance_group(access_token, subscription_id, resource_group,
                                 container_group_name):
    '''Get the JSON definition of a container group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        container_group_name (str): Name of container instance group.

    Returns:
        HTTP response. JSON body of container group.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups/',
                        container_group_name,
                        '?api-version=', CONTAINER_API])
    return do_get(endpoint, access_token)


def get_container_instance_logs(access_token, subscription_id, resource_group, container_group_name,
                                container_name=None):
    '''Get the container logs for containers in a container group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        container_group_name (str): Name of container instance group.
        container_name (str): Optional name of a container in the group.

    Returns:
        HTTP response. Container logs.
    '''
    if container_name is None:
        container_name = container_group_name
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups/',
                        container_group_name,
                        '/containers/', container_name, '/logs?api-version=', CONTAINER_API])
    return do_get(endpoint, access_token)


def list_container_instance_groups(access_token, subscription_id, resource_group):
    '''List the container groups in a resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.

    Returns:
        HTTP response. JSON list of container groups and their properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups',
                        '?api-version=', CONTAINER_API])
    return do_get(endpoint, access_token)


def list_container_instance_groups_sub(access_token, subscription_id):
    '''List the container groups in a subscription.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. JSON list of container groups and their properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.ContainerInstance/ContainerGroups',
                        '?api-version=', CONTAINER_API])
    return do_get(endpoint, access_token)
