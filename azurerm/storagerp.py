'''storagerp.py - azurerm functions for the Microsoft.Storage resource provider'''
import json
from .restfns import do_delete, do_get, do_put, do_post
from .settings import get_rm_endpoint, STORAGE_API


def create_storage_account(access_token, subscription_id, rgname, account_name, location,
                           storage_type='Standard_LRS'):
    '''Create a new storage account in the named resource group, with the named location.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        account_name (str): Name of the new storage account.
        location (str): Azure data center location. E.g. westus.
        storage_type (str): Premium or Standard, local or globally redundant.
            Defaults to Standard_LRS.

    Returns:
        HTTP response. JSON body of storage account properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '/providers/Microsoft.Storage/storageAccounts/', account_name,
                        '?api-version=', STORAGE_API])

    storage_body = {'location': location}
    storage_body['sku'] = {'name': storage_type}
    storage_body['kind'] = 'Storage'
    body = json.dumps(storage_body)
    return do_put(endpoint, body, access_token)


def delete_storage_account(access_token, subscription_id, rgname, account_name):
    '''Delete a storage account in the specified resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        account_name (str): Name of the new storage account.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '/providers/Microsoft.Storage/storageAccounts/', account_name,
                        '?api-version=', STORAGE_API])
    return do_delete(endpoint, access_token)


def get_storage_account(access_token, subscription_id, rgname, account_name):
    '''Get the properties for the named storage account.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        account_name (str): Name of the new storage account.

    Returns:
        HTTP response. JSON body of storage account properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '/providers/Microsoft.Storage/storageAccounts/', account_name,
                        '?api-version=', STORAGE_API])
    return do_get(endpoint, access_token)


def get_storage_account_keys(access_token, subscription_id, rgname, account_name):
    '''Get the access keys for the specified storage account.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        account_name (str): Name of the new storage account.

    Returns:
        HTTP response. JSON body of storage account keys.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '/providers/Microsoft.Storage/storageAccounts/', account_name,
                        '/listKeys',
                        '?api-version=', STORAGE_API])
    return do_post(endpoint, '', access_token)


def get_storage_usage(access_token, subscription_id):
    '''Returns storage usage and quota information for the specified subscription.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. JSON body of storage account usage.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Storage/usages',
                        '?api-version=', STORAGE_API])
    return do_get(endpoint, access_token)


def list_storage_accounts_rg(access_token, subscription_id, rgname):
    '''List the storage accounts in the specified resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.

    Returns:
        HTTP response. JSON body list of storage accounts.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '/providers/Microsoft.Storage/storageAccounts',
                        '?api-version=', STORAGE_API])
    return do_get(endpoint, access_token)


def list_storage_accounts_sub(access_token, subscription_id):
    '''List the storage accounts in the specified subscription.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. JSON body list of storage accounts.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Storage/storageAccounts',
                        '?api-version=', STORAGE_API])
    return do_get(endpoint, access_token)
