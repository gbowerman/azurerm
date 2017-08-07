'''amsrp.py - azurerm functions for the Microsoft.Media resource provider.'''
import json
from .restfns import do_get, do_post, do_put, do_delete
from .settings import get_rm_endpoint, MEDIA_API


def check_ms_name_availability(access_token, subscription_id, msname):
    '''Check media service name availability.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        msname (str): media service name.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/microsoft.media/CheckNameAvailability?',
                        'api-version=', MEDIA_API])
    ms_body = {'name': msname}
    ms_body['type'] = 'mediaservices'
    body = json.dumps(ms_body)
    return do_post(endpoint, body, access_token)


def create_media_service_rg(access_token, subscription_id, rgname, location, stoname, msname):
    '''Create a media service in a resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        location (str): Azure data center location. E.g. westus.
        stoname (str): Azure storage account name.
        msname (str): Media service name.

    Returns:
        HTTP response. JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', rgname,
                        '/providers/microsoft.media/mediaservices/', msname,
                        '?api-version=', MEDIA_API])
    ms_body = {'name': msname}
    ms_body['location'] = location
    sub_id_str = '/subscriptions/' + subscription_id + '/resourceGroups/' + rgname + \
        '/providers/Microsoft.Storage/storageAccounts/' + stoname
    storage_account = {'id': sub_id_str}
    storage_account['isPrimary'] = True
    properties = {'storageAccounts': [storage_account]}
    ms_body['properties'] = properties
    body = json.dumps(ms_body)
    return do_put(endpoint, body, access_token)


def delete_media_service_rg(access_token, subscription_id, rgname, msname):
    '''Delete a media service.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        msname (str): Media service name.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', rgname,
                        '/providers/microsoft.media/mediaservices/', msname,
                        '?api-version=', MEDIA_API])
    return do_delete(endpoint, access_token)


def list_media_endpoint_keys(access_token, subscription_id, rgname, msname):
    '''list the media endpoint keys in a media service

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        msname (str): Media service name.

    Returns:
        HTTP response. JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', rgname,
                        '/providers/microsoft.media/',
                        '/mediaservices/', msname,
                        '/listKeys?api-version=', MEDIA_API])
    return do_get(endpoint, access_token)


def list_media_services(access_token, subscription_id):
    '''List the media services in a subscription.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/microsoft.media/mediaservices?api-version=', MEDIA_API])
    return do_get(endpoint, access_token)


def list_media_services_rg(access_token, subscription_id, rgname):
    '''List the media services in a resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.

    Returns:
        HTTP response. JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', rgname,
                        '/providers/microsoft.media/mediaservices?api-version=', MEDIA_API])
    return do_get(endpoint, access_token)
