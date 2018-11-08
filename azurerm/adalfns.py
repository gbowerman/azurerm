'''adalfns - place to store azurerm functions which call adal routines'''
import json
import codecs
import os
import requests
from datetime import datetime as dt

import adal

from .settings import get_auth_endpoint, get_resource_endpoint


def get_access_token(tenant_id, application_id, application_secret):
    '''get an Azure access token using the adal library.

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
    '''Get an Azure authentication token from CLI's cache.

    Will only work if CLI local cache has an unexpired auth token (i.e. you ran 'az login'
        recently), or if you are running in Azure Cloud Shell (aka cloud console)

    Returns:
        An Azure authentication token string.
    '''

    # check if running in cloud shell, if so, pick up token from MSI_ENDPOINT
    if 'ACC_CLOUD' in os.environ and 'MSI_ENDPOINT' in os.environ:
        endpoint = os.environ['MSI_ENDPOINT']
        headers = {'Metadata': 'true'}
        body = {"resource": "https://management.azure.com/"}
        ret = requests.post(endpoint, headers=headers, data=body)
        return ret.json()['access_token']

    else: # not running cloud shell
        home = os.path.expanduser('~')
        sub_username = ""

        # 1st identify current subscription
        azure_profile_path = home + os.sep + '.azure' + os.sep + 'azureProfile.json'
        if os.path.isfile(azure_profile_path) is False:
            print('Error from get_access_token_from_cli(): Cannot find ' + azure_profile_path)
            return None
        with codecs.open(azure_profile_path, 'r', 'utf-8-sig') as azure_profile_fd:
            subs = json.load(azure_profile_fd)
        for sub in subs['subscriptions']:
            if sub['isDefault'] == True:
                sub_username = sub['user']['name']
        if sub_username == "":
            print('Error from get_access_token_from_cli(): Default subscription not found in ' +  \
                azure_profile_path)
            return None

        # look for acces_token
        access_keys_path = home + os.sep + '.azure' + os.sep + 'accessTokens.json'
        if os.path.isfile(access_keys_path) is False:
            print('Error from get_access_token_from_cli(): Cannot find ' + access_keys_path)
            return None
        with open(access_keys_path, 'r') as access_keys_fd:
            keys = json.load(access_keys_fd)

        # loop through accessTokens.json until first unexpired entry found
        for key in keys:
            if key['userId'] == sub_username:
                if 'accessToken' not in keys[0]:
                    print('Error from get_access_token_from_cli(): accessToken not found in ' + \
                        access_keys_path)
                    return None
                if 'tokenType' not in keys[0]:
                    print('Error from get_access_token_from_cli(): tokenType not found in ' + \
                        access_keys_path)
                    return None
                if 'expiresOn' not in keys[0]:
                    print('Error from get_access_token_from_cli(): expiresOn not found in ' + \
                        access_keys_path)
                    return None
                expiry_date_str = key['expiresOn']

                # check date and skip past expired entries
                if 'T' in expiry_date_str:
                    exp_date = dt.strptime(key['expiresOn'], '%Y-%m-%dT%H:%M:%S.%fZ')
                else:
                    exp_date = dt.strptime(key['expiresOn'], '%Y-%m-%d %H:%M:%S.%f')
                if exp_date < dt.now():
                    continue
                else:
                    return key['accessToken']

        # if dropped out of the loop, token expired
        print('Error from get_access_token_from_cli(): token expired. Run \'az login\'')
        return None
