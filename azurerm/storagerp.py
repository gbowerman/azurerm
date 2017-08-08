'''storagerp.py - azurerm functions for the Microsoft.Storage resource provider'''
import json
from .restfns import do_delete, do_get, do_put, do_post
from .settings import get_rm_endpoint, STORAGE_API


# create_storage_account(access_token, subscription_id, rgname, account_name, location)
def create_storage_account(access_token, subscription_id, rgname, account_name, location, storage_type='Standard_LRS'):
    '''Note: just standard storage for now. Could add a storageType argument later..
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
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '/providers/Microsoft.Storage/storageAccounts/', account_name,
                        '?api-version=', STORAGE_API])
    return do_delete(endpoint, access_token)


def get_storage_account(access_token, subscription_id, rgname, account_name):
    '''Get the properties for the named storage account.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '/providers/Microsoft.Storage/storageAccounts/', account_name,
                        '?api-version=', STORAGE_API])
    return do_get(endpoint, access_token)


def get_storage_account_keys(access_token, subscription_id, rgname, account_name):
    '''Get the access keys for the specified storage account.
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
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Storage/usages',
                        '?api-version=', STORAGE_API])
    return do_get(endpoint, access_token)


def list_storage_accounts_rg(access_token, subscription_id, rgname):
    '''List the storage accounts in the specified resource group.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '/providers/Microsoft.Storage/storageAccounts',
                        '?api-version=', STORAGE_API])
    return do_get(endpoint, access_token)


def list_storage_accounts_sub(access_token, subscription_id):
    '''List the storage accounts in the specified subscription.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Storage/storageAccounts',
                        '?api-version=', STORAGE_API])
    return do_get(endpoint, access_token)
