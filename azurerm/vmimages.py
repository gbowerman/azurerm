'''vmimages.py - azurerm functions for Microsoft.Compute RP publishers and images'''

from .restfns import do_get
from .settings import get_rm_endpoint, COMP_API


def list_offers(access_token, subscription_id, location, publisher):
    '''List available VM image offers from a publisher.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        location (str): Azure data center location. E.g. westus.

    Returns:
        HTTP response with JSON list of image offers.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/',
                        'locations/', location,
                        '/publishers/', publisher,
                        '/artifacttypes/vmimage/offers?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_publishers(access_token, subscription_id, location):
    '''List available image publishers for a location.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/',
                        'locations/', location,
                        '/publishers?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_skus(access_token, subscription_id, location, publisher, offer):
    '''List available VM image skus for a publisher offer.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/',
                        'locations/', location,
                        '/publishers/', publisher,
                        '/artifacttypes/vmimage/offers/', offer,
                        '/skus?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_sku_versions(access_token, subscription_id, location, publisher, offer, sku):
    '''List available versions for a given publisher's sku.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/',
                        'locations/', location,
                        '/publishers/', publisher,
                        '/artifacttypes/vmimage/offers/', offer,
                        '/skus/', sku,
                        '/versions?api-version=', COMP_API])
    return do_get(endpoint, access_token)
