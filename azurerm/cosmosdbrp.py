'''cosmosdbrp.py - azurerm functions for the Microsoft.DocumentDB resource provider'''
import json

from .restfns import do_post, do_put
from .settings import COSMOSDB_API, get_rm_endpoint


def create_cosmosdb_account(access_token, subscription_id, rgname, account_name, location,
                            cosmosdb_kind):
    '''Create a new Cosmos DB account in the named resource group, with the named location.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        account_name (str): Name of the new Cosmos DB account.
        location (str): Azure data center location. E.g. westus.
        cosmosdb_kind (str): Database type. E.g. GlobalDocumentDB.

    Returns:
        HTTP response. JSON body of storage account properties.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '/providers/Microsoft.DocumentDB/databaseAccounts/', account_name,
                        '?api-version=', COSMOSDB_API])

    cosmosdb_body = {'location': location,
                     'kind': cosmosdb_kind,
                     'properties': {'databaseAccountOfferType': 'Standard',
                                    'locations': [{'failoverPriority': 0,
                                                   'locationName': location}]}}
    body = json.dumps(cosmosdb_body)
    return do_put(endpoint, body, access_token)


def get_cosmosdb_account_keys(access_token, subscription_id, rgname, account_name):
    '''Get the access keys for the specified Cosmos DB account.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        account_name (str): Name of the Cosmos DB account.

    Returns:
        HTTP response. JSON body of Cosmos DB account keys.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '/providers/Microsoft.DocumentDB/databaseAccounts/', account_name,
                        '/listKeys',
                        '?api-version=', COSMOSDB_API])
    return do_post(endpoint, '', access_token)
