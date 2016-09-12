# amsrp.py - azurerm functions for the Microsoft.Media resource provider

from .restfns import do_get, do_post, do_put, do_delete
from .settings import azure_rm_endpoint, MEDIA_API


# check_name_availability of a media service name(access_token, subscription_id, rgname)
# check the media service name availability in a rgname and msname
def check_media_service_name_availability(access_token, subscription_id, name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/microsoft.media/CheckNameAvailability?api-version=', MEDIA_API])
    body = '{"name": "' + name + '", "type":"mediaservices"}'
    return do_post(endpoint, body, access_token)

# create_media_service_rg(access_token, subscription_id, rgname)
# create the media service in a rgname
def create_media_service_rg(access_token, subscription_id, rgname, location, stoname, name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', rgname,
                        '/providers/microsoft.media/mediaservices/' + name + '?api-version=', MEDIA_API])

    body = '{"name":"' + name + '", "location":"' + location + '", "properties":{  "storageAccounts":[  {  "id":"/subscriptions/' + subscription_id + '/resourceGroups/' + rgname + '/providers/Microsoft.Storage/storageAccounts/' + stoname + '", "isPrimary":true } ] } }'
    return do_put(endpoint, body, access_token)


# delete_media_service_rg(access_token, subscription_id, rgname)
# delete the media service in a rgname
def delete_media_service_rg(access_token, subscription_id, rgname, location, stoname, name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', rgname,
                        '/providers/microsoft.media/mediaservices/' + name + '?api-version=', MEDIA_API])

    return do_delete(endpoint, access_token)


# list_media_endpoint_keys in a resrouce group(access_token, subscription_id, rgname, msname)
# list the media endpoint keys in a rgname and msname
def list_media_endpoint_keys(access_token, subscription_id, rgname, msname):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', rgname,
                        '/providers/microsoft.media/',
                        '/mediaservices/', msname,
                        '/listKeys?api-version=', MEDIA_API])
    return do_get(endpoint, access_token)


# list_media_services(access_token, subscription_id)
# list the media services in a subscription_id
def list_media_services(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/microsoft.media/mediaservices?api-version=', MEDIA_API])
    return do_get(endpoint, access_token)


# list_media_services_rg in a resrouce group(access_token, subscription_id, rgname)
# list the media services in a rgname
def list_media_services_rg(access_token, subscription_id, rgname):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', rgname,
                        '/providers/microsoft.media/mediaservices?api-version=', MEDIA_API])
    return do_get(endpoint, access_token)
