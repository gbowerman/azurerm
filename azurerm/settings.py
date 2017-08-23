'''settings.py - place to store constants for azurerm'''
import os

# public defaults for authentication and resource endpoints
AZURE_RM_ENDPOINT = 'https://management.azure.com'
AZURE_AUTH_ENDPOINT = 'https://login.microsoftonline.com/'
AZURE_RESOURCE_ENDPOINT = 'https://management.core.windows.net/'

ACS_API = '2017-01-31'
BASE_API = '2016-09-01'
COMP_API = '2017-03-30'
CONTAINER_API = '2017-08-01-preview'
COSMOSDB_API = '2015-04-08'
INSIGHTS_API = '2015-04-01'
INSIGHTS_METRICS_API = '2016-03-01'
INSIGHTS_PREVIEW_API = '2016-06-01'
MEDIA_API = '2015-10-01'
NETWORK_API = '2017-04-01'
STORAGE_API = '2016-01-01'

def get_rm_endpoint():
    '''Set Azure Resource Manager endpoint by environment variable, else return default value.

    These functions facilitate the use of national and isolated clouds by allowing endpoints to
    be set dynamically. The default settings, if no environment varibles are used,
    are for public cloud.
    '''
    rm_endpoint = os.environ.get('AZURE_RM_ENDPOINT')
    if rm_endpoint is None:
        return AZURE_RM_ENDPOINT
    else:
        return rm_endpoint


def get_auth_endpoint():
    '''Set Azure auth endpoint by environment variable, else return default value.
    '''
    auth_endpoint = os.environ.get('AZURE_AUTH_ENDPOINT')
    if auth_endpoint is None:
        return AZURE_AUTH_ENDPOINT
    else:
        return auth_endpoint


def get_resource_endpoint():
    '''Set Azure reousrce endpoint by environment variable, else return default value.
    '''
    resource_endpoint = os.environ.get('AZURE_RESOURCE_ENDPOINT')
    if resource_endpoint is None:
        return AZURE_RESOURCE_ENDPOINT
    else:
        return resource_endpoint
