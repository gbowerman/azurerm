''' adalfns - place to store azurerm functions which call adal routines'''
import json
import os
from datetime import datetime as dt

import adal

from .settings import get_auth_endpoint, get_resource_endpoint


def get_access_token(tenant_id, application_id, application_secret):
    '''get an Azure access token using the adal library

    Args:
        tenant_id (str): Tenant id of the user's account.
        application_id (str): Application id of a Service Principal account.
        application_secret (str): Application secret (password) of the Service Principal account.

    Returns:
        An Azure authentication token string.
    '''
    context = adal.AuthenticationContext(
        get_auth_endpoint() + tenant_id, api_version=None)
    token_response = context.acquire_token_with_client_credentials(
        get_resource_endpoint(), application_id, application_secret)
    return token_response.get('accessToken')


def get_access_token_from_cli():
    '''Get an Azure authentication token from CLI's local cache

    Will only work if CLI local cache has an unexpired auth token (i.e. you ran 'az login' 
        recently)

    Returns:
        An Azure authentication token string.
    '''
    home = os.path.expanduser('~')
    access_keys_path = home + os.sep + '.azure' + os.sep + 'accessTokens.json'
    if os.path.isfile(access_keys_path) is False:
        print('Error from get_access_token_from_cli(): Cannot find ' + access_keys_path)
        return None
    with open(access_keys_path, 'r') as access_keys_fd:
        keys = json.load(access_keys_fd)
    if 'accessToken' not in keys[0]:
        print('Error from get_access_token_from_cli(): accessToken not found in ' + \
            access_keys_path)
        return None
    if 'expiresOn' not in keys[0]:
        print('Error from get_access_token_from_cli(): expiresOn not found in ' + \
            access_keys_path)
        return None
    if 'tokenType' not in keys[0]:
        print('Error from get_access_token_from_cli(): tokenType not found in ' + \
            access_keys_path)
        return None
    expiry_date_str = keys[0]['expiresOn']
    if 'T' in expiry_date_str:
        exp_date = dt.strptime(keys[0]['expiresOn'], '%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        exp_date = dt.strptime(keys[0]['expiresOn'], '%Y-%m-%d %H:%M:%S.%f')
    if exp_date < dt.now():
        print('Error from get_access_token_from_cli(): token expired. Run \'az login\'')
        return None
    return keys[0]['accessToken']
