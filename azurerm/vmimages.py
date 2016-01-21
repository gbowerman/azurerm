# vmimages.py - azurerm functions for Microsoft.Compute RP publishers and images
from .settings import azure_rm_endpoint, COMP_API
from .restfns import do_delete, do_get, do_put, do_patch, do_post

# list_publishers(access_token, subscription_id, location)
# list available publishers for a location
def list_publishers(access_token, subscription_id, location):
    endpoint = ''.join([azure_rm_endpoint,
                         '/subscriptions/', subscription_id,
                         '/providers/Microsoft.Compute/',
                         'locations/', location,
                         '/publishers?api-version=', COMP_API])
    return do_get(endpoint, access_token)

# list_images(access_token, subscription_id, location, publisher)
# list available publishers for a location
def list_offers(access_token, subscription_id, location, publisher):
    endpoint = ''.join([azure_rm_endpoint,
                         '/subscriptions/', subscription_id,
                         '/providers/Microsoft.Compute/',
                         'locations/', location,
                         '/publishers/', publisher,
                         '/artifacttypes/vmimage/offers?api-version=', COMP_API])
    return do_get(endpoint, access_token)

# list_images(access_token, subscription_id, location, publisher)
# list available publishers for a location
def list_skus(access_token, subscription_id, location, publisher, offer):
    endpoint = ''.join([azure_rm_endpoint,
                         '/subscriptions/', subscription_id,
                         '/providers/Microsoft.Compute/',
                         'locations/', location,
                         '/publishers/', publisher,
                         '/artifacttypes/vmimage/offers/', offer,
                         '/skus?api-version=', COMP_API])
    return do_get(endpoint, access_token)
