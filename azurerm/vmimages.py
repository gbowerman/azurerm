# vmimages.py - azurerm functions for Microsoft.Compute RP publishers and images

from .restfns import do_get
from .settings import azure_rm_endpoint, COMP_API


# list_offers(access_token, subscription_id, location, publisher)
# list available VM image offers from a publisher
def list_offers(access_token, subscription_id, location, publisher):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/',
                        'locations/', location,
                        '/publishers/', publisher,
                        '/artifacttypes/vmimage/offers?api-version=', COMP_API])
    return do_get(endpoint, access_token)


# list_publishers(access_token, subscription_id, location)
# list available image publishers for a location
def list_publishers(access_token, subscription_id, location):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/',
                        'locations/', location,
                        '/publishers?api-version=', COMP_API])
    return do_get(endpoint, access_token)


# list_skus(access_token, subscription_id, location, publisher, offer)
# list available VM image skus for a publisher offer
def list_skus(access_token, subscription_id, location, publisher, offer):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/',
                        'locations/', location,
                        '/publishers/', publisher,
                        '/artifacttypes/vmimage/offers/', offer,
                        '/skus?api-version=', COMP_API])
    return do_get(endpoint, access_token)


# list_sku_versions(access_token, subscription_id, location, publisher, offer, sku)
# list available versions for a given publisher's sku
def list_sku_versions(access_token, subscription_id, location, publisher, offer, sku):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/Microsoft.Compute/',
                        'locations/', location,
                        '/publishers/', publisher,
                        '/artifacttypes/vmimage/offers/', offer,
                        '/skus/', sku,
                        '/versions?api-version=', COMP_API])
    return do_get(endpoint, access_token)
