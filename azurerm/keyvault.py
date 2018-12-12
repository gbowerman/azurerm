'''keyvault.py - azurerm functions for the Microsoft.Keyvault resource provider'''
import json
from .restfns import do_delete, do_get, do_get_next, do_put, do_post
from .subfns import list_tenants
from .settings import get_rm_endpoint, KEYVAULT_API


def create_keyvault(access_token, subscription_id, rgname, vault_name, location,
                    template_deployment=True, tenant_id=None, object_id=None):
    '''Create a new key vault in the named resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        vault_name (str): Name of the new key vault.
        location (str): Azure data center location. E.g. westus2.
        template_deployment (boolean): Whether to allow deployment from template.
        tenant_id (str): Optionally specify a tenant ID (otherwise picks first response) from
                         ist_tenants().
        object_id (str): Optionally specify an object ID representing user or principal for the
                         access policy.

    Returns:
        HTTP response. JSON body of key vault properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '/providers/Microsoft.KeyVault/vaults/', vault_name,
                        '?api-version=', KEYVAULT_API])
    # get tenant ID if not specified
    if tenant_id is None:
        ret = list_tenants(access_token)
        tenant_id = ret['value'][0]['tenantId']
    # if object_id is None:
    access_policies = [{'tenantId': tenant_id, 'objectId': object_id,
                        'permissions': {
                            'keys': ['get', 'create', 'delete', 'list', 'update', 'import',
                                     'backup', 'restore', 'recover'],
                            'secrets': ['get', 'list', 'set', 'delete', 'backup', 'restore',
                                        'recover'],
                            'certificates': ['get', 'list', 'delete', 'create', 'import', 'update',
                                             'managecontacts', 'getissuers', 'listissuers',
                                             'setissuers', 'deleteissuers', 'manageissuers',
                                             'recover'],
                            'storage': ['get', 'list', 'delete', 'set', 'update', 'regeneratekey',
                                        'setsas', 'listsas', 'getsas', 'deletesas']
                        }}]
    vault_properties = {'tenantId': tenant_id, 'sku': {'family': 'A', 'name': 'standard'},
                        'enabledForTemplateDeployment': template_deployment,
                        'accessPolicies': access_policies}
    vault_body = {'location': location, 'properties': vault_properties}
    body = json.dumps(vault_body)
    return do_put(endpoint, body, access_token)


def delete_keyvault(access_token, subscription_id, rgname, vault_name):
    '''Deletes a key vault in the named resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        vault_name (str): Name of the new key vault.

    Returns:
        HTTP response. 200 OK.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '/providers/Microsoft.KeyVault/vaults/', vault_name,
                        '?api-version=', KEYVAULT_API])
    return do_delete(endpoint, access_token)


def get_keyvault(access_token, subscription_id, rgname, vault_name):
    '''Gets details about the named key vault.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        vault_name (str): Name of the key vault.

    Returns:
        HTTP response. JSON body of key vault properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '/providers/Microsoft.KeyVault/vaults/', vault_name,
                        '?api-version=', KEYVAULT_API])
    return do_get(endpoint, access_token)


def list_keyvaults(access_token, subscription_id, rgname):
    '''Lists key vaults in the named resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.

    Returns:
        HTTP response. 200 OK.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '/providers/Microsoft.KeyVault/vaults',
                        '?api-version=', KEYVAULT_API])
    return do_get_next(endpoint, access_token)


def list_keyvaults_sub(access_token, subscription_id):
    '''Lists key vaults belonging to this subscription.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. 200 OK.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.KeyVault/vaults',
                        '?api-version=', KEYVAULT_API])
    return do_get_next(endpoint, access_token)