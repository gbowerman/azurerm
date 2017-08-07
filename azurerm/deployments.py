'''deployments.py - azurerm functions for Deployments'''

from .restfns import do_get
from .settings import get_rm_endpoint, BASE_API


def list_deployment_operations(access_token, subscription_id, rg_name, deployment_name):
    '''List all operations involved in a given deployment.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rg_name (str): Azure resource group name.

    Returns:
        HTTP response. JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rg_name,
                        '/providers/Microsoft.Resources/deployments/', deployment_name,
                        '/operations',
                        '?api-version=', BASE_API])
    return do_get(endpoint, access_token)


def show_deployment(access_token, subscription_id, rg_name, deployment_name):
    '''Show details for a named deployment.abs

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rg_name (str): Azure resource group name.

    Returns:
        HTTP response. JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rg_name,
                        '/providers/microsoft.resources/deployments/', deployment_name,
                        '?api-version=', BASE_API])
    return do_get(endpoint, access_token)
