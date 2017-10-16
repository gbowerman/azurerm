'''keyvault.py - azurerm functions for the Microsoft.Keyvault resource provider'''
import json
from .restfns import do_delete, do_get, do_put, do_post
from .settings import get_rm_endpoint, KEYVAULT_API


def create_keyvault(access_token, subscription_id, rgname, vault_name, location):
    '''Create a new key vault in the named resource group.
    PUT /Microsoft.KeyVault/vaults/{vaultName}?api-version=2016-10-01
    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        vault_name (str): Name of the new key vault.
        location (str): Azure data center location. E.g. westus.

    Returns:
        HTTP response. JSON body of key vault properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '/providers/Microsoft.KeyVault/vaults/', vault_name,
                        '?api-version=', KEYVAULT_API])

    vault_body = {'location': location}
    body = json.dumps(vault_body)
    return do_put(endpoint, body, access_token)
