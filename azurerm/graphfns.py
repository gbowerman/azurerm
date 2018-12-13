'''graphfns - functions to call Microsoft graph functions
   
     - Some functions depend on Azure cloud shell/Azure VMs for MSI endpoint
'''
import requests
import os

from .settings import GRAPH_RESOURCE_HOST


def get_graph_token_from_msi():
    '''get a Microsoft Graph access token using Azure Cloud Shell's MSI_ENDPOINT.

        Notes: 
        The auth token returned by this function is not an Azure auth token. Use it for querying
        the Microsoft Graph API.
        This function only works in an Azure cloud shell or virtual machine.

    Returns:
        A Microsoft Graph authentication token string.
    '''
    if 'ACC_CLOUD' in os.environ and 'MSI_ENDPOINT' in os.environ:
        endpoint = os.environ['MSI_ENDPOINT']
    else:
        return None
    
    headers = {'Metadata': 'true'}
    body = {"resource": 'https://' + GRAPH_RESOURCE_HOST + '/'}
    ret = requests.post(endpoint, headers=headers, data=body)
    return ret.json()['access_token']


def get_object_id_from_graph(access_token=None):
    '''Return the object ID for the Graph user who owns the access token.

    Args:
        access_token (str): A Microsoft Graph access token. (Not an Azure access token.)
                            If not provided, attempt to get it from MSI_ENDPOINT.

    Returns:
        An object ID string for a user or service principal.
    '''
    if access_token is None:
        access_token = get_graph_token_from_msi()

    endpoint = 'https://' + GRAPH_RESOURCE_HOST + '/v1.0/me/'
    headers = {'Authorization': 'Bearer ' + access_token, 'Host': GRAPH_RESOURCE_HOST}
    ret = requests.get(endpoint, headers=headers)
    print(ret)
    return ret.json()['id']
