# deployments.py - azurerm functions for Deployments

from .restfns import do_get
from .settings import azure_rm_endpoint, BASE_API
 

# list_deployment_operations(access_token, subscription_id, rg_name, deployment_name)
# lists all operations involved in a given deployment
def list_deployment_operations(access_token, subscription_id, rg_name, deployment_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rg_name,
                        '/providers/Microsoft.Resources/deployments/', deployment_name,
                        '/operations',
                        '?api-version=', BASE_API])
    return do_get(endpoint, access_token)


def show_deployment(access_token, subscription_id, rg_name, deployment_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rg_name,
                        '/providers/microsoft.resources/deployments/', deployment_name,
                        '?api-version=', BASE_API])
    return do_get(endpoint, access_token)
