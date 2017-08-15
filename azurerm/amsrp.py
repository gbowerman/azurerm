'''amsrp.py - azurerm functions for the Microsoft.Media resource provider and AMS Rest Interface.'''

import json
import urllib
import requests
from .restfns import do_ams_auth, do_ams_get, do_ams_post, do_ams_put, do_ams_delete, do_ams_patch, do_ams_sto_put, do_ams_get_url
from .settings import get_rm_endpoint, ams_rest_endpoint, ams_auth_endpoint, MEDIA_API

def check_media_service_name_availability(access_token, subscription_id, msname):
    '''Check media service name availability.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        msname (str): media service name.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/microsoft.media/CheckNameAvailability?',
                        'api-version=', MEDIA_API])
    ms_body = {'name': msname}
    ms_body['type'] = 'mediaservices'
    body = json.dumps(ms_body)
    return do_ams_post(endpoint, body, access_token)


def create_media_service_rg(access_token, subscription_id, rgname, location, stoname, msname):
    '''Create a media service in a resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        location (str): Azure data center location. E.g. westus.
        stoname (str): Azure storage account name.
        msname (str): Media service name.

    Returns:
        HTTP response. JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', rgname,
                        '/providers/microsoft.media/mediaservices/', msname,
                        '?api-version=', MEDIA_API])
    ms_body = {'name': msname}
    ms_body['location'] = location
    sub_id_str = '/subscriptions/' + subscription_id + '/resourceGroups/' + rgname + \
        '/providers/Microsoft.Storage/storageAccounts/' + stoname
    storage_account = {'id': sub_id_str}
    storage_account['isPrimary'] = True
    properties = {'storageAccounts': [storage_account]}
    ms_body['properties'] = properties
    body = json.dumps(ms_body)
    return do_ams_put(endpoint, body, access_token)


def delete_media_service_rg(access_token, subscription_id, rgname, msname):
    '''Delete a media service.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        msname (str): Media service name.

    Returns:
        HTTP response.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', rgname,
                        '/providers/microsoft.media/mediaservices/', msname,
                        '?api-version=', MEDIA_API])
    return do_ams_delete(endpoint, access_token)


def list_media_endpoint_keys(access_token, subscription_id, rgname, msname):
    '''list the media endpoint keys in a media service

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        msname (str): Media service name.

    Returns:
        HTTP response. JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', rgname,
                        '/providers/microsoft.media/',
                        '/mediaservices/', msname,
                        '/listKeys?api-version=', MEDIA_API])
    return do_ams_get(endpoint, access_token)


def list_media_services(access_token, subscription_id):
    '''List the media services in a subscription.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/microsoft.media/mediaservices?api-version=', MEDIA_API])
    return do_ams_get(endpoint, access_token)


def list_media_services_rg(access_token, subscription_id, rgname):
    '''List the media services in a resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.

    Returns:
        HTTP response. JSON body.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', rgname,
                        '/providers/microsoft.media/mediaservices?api-version=', MEDIA_API])
    return do_ams_get(endpoint, access_token)


"""
Copyright (c) 2016, Marcelo Leal
Description: Simple Azure Media Services Rest Python library
License: MIT (see LICENSE.txt file for details)
"""

# get_access_token(accountname, accountkey)
# get access token with ams
def get_ams_access_token(accountname, accountkey):
    accountkey_encoded = urllib.parse.quote(accountkey, safe='')
    body = "grant_type=client_credentials&client_id=" + accountname + \
	"&client_secret=" + accountkey_encoded + " &scope=urn%3aWindowsAzureMediaServices"
    return do_ams_auth(ams_auth_endpoint, body)

# get_url(access_token)
# get an specific url
def get_url(access_token, endpoint=ams_rest_endpoint, flag=True):
    return do_ams_get_url(endpoint, access_token, flag)

# list_media_asset(access_token, oid="")
# list a media asset(s)
def list_media_asset(access_token, oid=""):
    path = '/Assets'
    return helper_list(access_token, oid, path)

# list_content_keys(access_token, oid="")
# list the content key(s)
def list_content_key(access_token, oid=""):
    path = '/ContentKeys'
    return helper_list(access_token, oid, path)

# list_contentkey_authorization_policy(access_token, oid="")
# list content key authorization policy(ies)
def list_contentkey_authorization_policy(access_token, oid=""):
    path = '/ContentKeyAuthorizationPolicies'
    return helper_list(access_token, oid, path)

# list_contentkey_authorization_policy_options(access_token, oid="")
# list content key authorization policy options
def list_contentkey_authorization_policy_options(access_token, oid=""):
    path = '/ContentKeyAuthorizationPolicyOptions'
    return helper_list(access_token, oid, path)

# list_media_processor(access_token, oid="")
# list the media processor(s)
def list_media_processor(access_token, oid=""):
    path = '/MediaProcessors'
    return helper_list(access_token, oid, path)

# list_asset_accesspolicy(access_token, oid="")
# list a asset access policy(ies)
def list_asset_accesspolicy(access_token, oid=""):
    path = '/AccessPolicies'
    return helper_list(access_token, oid, path)

# list_sas_locator(access_token, oid="")
# list a sas locator(s)
def list_sas_locator(access_token, oid=""):
    path = '/Locators'
    return helper_list(access_token, oid, path)

# list_media_job(access_token, oid="")
# list a media job(s)
def list_media_job(access_token, oid=""):
    path = '/Jobs'
    return helper_list(access_token, oid, path)

# list_asset_delivery_policy(access_token, oid="")
# list an asset delivery policy(ies)
def list_asset_delivery_policy(access_token, oid=""):
    path = '/AssetDeliveryPolicies'
    return helper_list(access_token, oid, path)

# list_streaming_endpoint(access_token, oid="")
# list streaming endpoint(s)
def list_streaming_endpoint(access_token, oid=""):
    path = '/StreamingEndpoints'
    return helper_list(access_token, oid, path)

# delete_streaming_endpoint(access_token, oid)
# delete a streaming endpoint
def delete_streaming_endpoint(access_token, oid):
    path = '/StreamingEndpoints'
    return helper_delete(access_token, oid, path)

# delete_asset_delivery_policy(access_token, oid)
# delete a asset delivery policy
def delete_asset_delivery_policy(access_token, oid):
    path = '/AssetDeliveryPolicies'
    return helper_delete(access_token, oid, path)

# delete_asset_accesspolicy(access_token, oid)
# delete a asset access policy
def delete_asset_accesspolicy(access_token, oid):
    path = '/AccessPolicies'
    return helper_delete(access_token, oid, path)

# delete_sas_locator(access_token, oid)
# delete a sas locator
def delete_sas_locator(access_token, oid):
    path = '/Locators'
    return helper_delete(access_token, oid, path)

# delete_content_key(access_token, oid)
# delete a content key
def delete_content_key(access_token, oid):
    path = '/ContentKeys'
    return helper_delete(access_token, oid, path)

# delete_contentkey_authorization_policy(access_token, oid)
# delete a content key authorization policy
def delete_contentkey_authorization_policy(access_token, oid):
    path = '/ContentKeyAuthorizationPolicies'
    return helper_delete(access_token, oid, path)

# delete_contentkey_authorization_policy_options(access_token, oid)
# delete content key authorization policy options
def delete_contentkey_authorization_policy_options(access_token, oid):
    path = '/ContentKeyAuthorizationPolicyOptions'
    return helper_delete(access_token, oid, path)

# delete_media_asset(access_token, oid)
# delete a media asset
def delete_media_asset(access_token, oid):
    path = '/Assets'
    return helper_delete(access_token, oid, path)

# create_media_asset(access_token, name, options="0")
# create a media asset
def create_media_asset(access_token, name, options="0"):
    path = '/Assets'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = '{"Name": "' + name + '", "Options": "' + str(options) + '"}'
    return do_ams_post(endpoint, path, body, access_token)

# create_media_assetfile(access_token, parent_asset_id, name, is_primary="false", is_encrypted="false", encryption_scheme="None", encryptionkey_id="None")
# create a media assetfile
def create_media_assetfile(access_token, parent_asset_id, name, is_primary="false", is_encrypted="false", encryption_scheme="None", encryptionkey_id="None"):
    path = '/Files'
    endpoint = ''.join([ams_rest_endpoint, path])
    if (encryption_scheme == "StorageEncryption"):
    	body = '{ \
			"IsEncrypted": "' + is_encrypted + '", \
			"EncryptionScheme": "' + encryption_scheme + '", \
			"EncryptionVersion": "' + "1.0" + '", \
			"EncryptionKeyId": "' + encryptionkey_id + '", \
			"IsPrimary": "' + is_primary + '", \
			"MimeType": "video/mp4", \
			"Name": "' + name + '", \
			"ParentAssetId": "' + parent_asset_id + '" \
		}'
    else:
    	body = '{ \
			"IsPrimary": "' + is_primary + '", \
			"MimeType": "video/mp4", \
			"Name": "' + name + '", \
			"ParentAssetId": "' + parent_asset_id + '" \
		}'
    return do_ams_post(endpoint, path, body, access_token)

# create_sas_locator(access_token, asset_id, accesspolicy_id)
# create a sas locator
def create_sas_locator(access_token, asset_id, accesspolicy_id):
    path = '/Locators'
    endpoint = ''.join([ams_rest_endpoint, path])
    #body = '{"AccessPolicyId":"' + accesspolicy_id + '", "AssetId":"' + asset_id + '", "StartTime":"' + starttime + '", "Type":1 }'
    body = '{ \
		"AccessPolicyId":"' + accesspolicy_id + '", \
		"AssetId":"' + asset_id + '", \
		"Type":1 \
	}'
    return do_ams_post(endpoint, path, body, access_token)

# create_asset_delivery_policy(access_token, asset_id, accesspolicy_id)
# create an asset delivery policy
def create_asset_delivery_policy(access_token, ams_account):
    path = '/AssetDeliveryPolicies'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = '{ \
		"Name":"AssetDeliveryPolicy", \
		"AssetDeliveryProtocol":"4", \
		"AssetDeliveryPolicyType":"3", \
		"AssetDeliveryConfiguration":"[{ \
			\\"Key\\":\\"2\\", \
			\\"Value\\":\\"https://' + ams_account + '.keydelivery.mediaservices.windows.net/\\"}]" \
	}'
    return do_ams_post(endpoint, path, body, access_token)

# create_media_task(access_token, processor_id, asset_id, content)
# create a media task
def create_media_task(access_token, processor_id, asset_id, content):
    path = '/Tasks'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = content
    return do_ams_post(endpoint, path, body, access_token)

# create_media_job(access_token, processor_id, asset_id, content)
# create a media job
def create_media_job(access_token, processor_id, asset_id, content):
    path = '/Jobs'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = content
    return do_ams_post(endpoint, path, body, access_token)

# create_contentkey_authorization_policy(access_token, processor_id, asset_id, content)
# create content key authorization policy
def create_contentkey_authorization_policy(access_token, content):
    path = '/ContentKeyAuthorizationPolicies'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = content
    return do_ams_post(endpoint, path, body, access_token)

# create_contentkey_authorization_policy_options(access_token, processor_id, asset_id, content)
# create content key authorization policy options
def create_contentkey_authorization_policy_options(access_token, key_delivery_type="2", name="HLS Open Authorization Policy", key_restriction_type="0"):
    path = '/ContentKeyAuthorizationPolicyOptions'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = '{ \
		"Name":"policy",\
		"KeyDeliveryType":2, \
		"KeyDeliveryConfiguration":"", \
			"Restrictions":[{ \
			"Name":"' + name + '", \
			"KeyRestrictionType":0, \
			"Requirements":null \
		}] \
	}'
    return do_ams_post(endpoint, path, body, access_token, "json_only")

# create_ondemand_streaming_locator(access_token, encoded_asset_id, asset_id, pid, starttime="None")
# create an ondemand streaming locator
def create_ondemand_streaming_locator(access_token, encoded_asset_id, pid, starttime=None):
    path = '/Locators'
    endpoint = ''.join([ams_rest_endpoint, path])
    if(starttime == None):
    	body = '{ \
			"AccessPolicyId":"' + pid + '", \
			"AssetId":"' + encoded_asset_id + '", \
			"Type": "2" \
		}' 
    else:
    	body = '{ \
			"AccessPolicyId":"' + pid + '", \
			"AssetId":"' + encoded_asset_id + '", \
			"StartTime":"' + str(starttime) + '", \
			"Type": "2" \
		}' 
    return do_ams_post(endpoint, path, body, access_token, "json_only")

# create_asset_accesspolicy(access_token, duration)
# create an asset access policy
def create_asset_accesspolicy(access_token, name, duration, permission="1"):
    path = '/AccessPolicies'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = '{ \
		"Name": "' + str(name) + '", \
		"DurationInMinutes": "' + duration + '", \
		"Permissions": "' + permission + '" \
	}'
    return do_ams_post(endpoint, path, body, access_token)

# create_streaming_endpoint(access_token, name, options="0")
# create a streaming endpoint
def create_streaming_endpoint(access_token, name, description="New Streaming Endpoint", scale_units="1"):
    path = '/StreamingEndpoints'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = '{ \
		"Id":null, \
		"Name":"' + name + '", \
		"Description":"' + description + '", \
		"Created":"0001-01-01T00:00:00", \
		"LastModified":"0001-01-01T00:00:00", \
		"State":null, \
		"HostName":null, \
		"ScaleUnits":"' + scale_units + '", \
		"CrossSiteAccessPolicies":{ \
			"ClientAccessPolicy":"<access-policy><cross-domain-access><policy><allow-from http-request-headers=\\"*\\"><domain uri=\\"http://*\\" /></allow-from><grant-to><resource path=\\"/\\" include-subpaths=\\"false\\" /></grant-to></policy></cross-domain-access></access-policy>", \
			"CrossDomainPolicy":"<?xml version=\\"1.0\\"?><!DOCTYPE cross-domain-policy SYSTEM \\"http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd\\"><cross-domain-policy><allow-access-from domain=\\"*\\" /></cross-domain-policy>" \
		} \
	}'
    return do_ams_post(endpoint, path, body, access_token)

# scale_streaming_endpoint(access_token, streaming_endpoint_id, scale_units)
# scale a scale unit
def scale_streaming_endpoint(access_token, streaming_endpoint_id, scale_units):
    path = '/StreamingEndpoints'
    full_path = ''.join([path, "('", streaming_endpoint_id, "')", "/Scale"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    body = '{"scaleUnits": "' + str(scale_units) + '"}'
    return do_ams_post(endpoint, full_path_encoded, body, access_token)

# link_asset_content_key(access_token, asset_id, encryptionkey_id)
# link an asset with a content key
def link_asset_content_key(access_token, asset_id, encryptionkey_id, ams_redirected_rest_endpoint):
    path = '/Assets'
    full_path = ''.join([path, "('", asset_id, "')", "/$links/ContentKeys"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    uri = ''.join([ams_redirected_rest_endpoint, 'ContentKeys', "('", encryptionkey_id, "')"])
    body = '{"uri": "' + uri + '"}'
    return do_ams_post(endpoint, full_path_encoded, body, access_token)

# link_asset_deliver_policy(access_token, asset_id, encryptionkey_id)
# link an asset with a delivery policy
def link_asset_delivery_policy(access_token, asset_id, adp_id, ams_redirected_rest_endpoint):
    path = '/Assets'
    full_path = ''.join([path, "('", asset_id, "')", "/$links/DeliveryPolicies"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    uri = ''.join([ams_redirected_rest_endpoint, 'AssetDeliveryPolicies', "('", adp_id, "')"])
    body = '{"uri": "' + uri + '"}'
    return do_ams_post(endpoint, full_path_encoded, body, access_token)

# link_contentkey_authorization_policy(access_token, ckap_id, options_id, encryptionkey_id)
# link content key aurhorization policy with options
def link_contentkey_authorization_policy(access_token, ckap_id, options_id, ams_redirected_rest_endpoint):
    path = '/ContentKeyAuthorizationPolicies'
    full_path = ''.join([path, "('", ckap_id, "')", "/$links/Options"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    uri = ''.join([ams_redirected_rest_endpoint, 'ContentKeyAuthorizationPolicyOptions', "('", options_id, "')"])
    body = '{"uri": "' + uri + '"}'
    return do_ams_post(endpoint, full_path_encoded, body, access_token, "json_only", "1.0;NetFx")

# add_authorization_policy(access_token, oid)
# add a authorization policy
def add_authorization_policy(access_token, ck_id, oid):
    path = '/ContentKeys'
    body = '{"AuthorizationPolicyId":"' + oid + '"}'
    return helper_add(access_token, ck_id, path, body)

# update_media_assetfile(access_token, parent_asset_id, asset_id, content_length, name)
# update a media assetfile
def update_media_assetfile(access_token, parent_asset_id, asset_id, content_length, name):
    path = '/Files'
    full_path = ''.join([path, "('", asset_id, "')"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    body = '{ \
		"ContentFileSize": "' + str(content_length) + '", \
		"Id": "' + asset_id + '", \
		"MimeType": "video/mp4", \
		"Name": "' + name + '", \
		"ParentAssetId": "' + parent_asset_id + '" \
	}'
    return do_ams_patch(endpoint, full_path_encoded, body, access_token)

# get_delivery_url(access_token, ck_id, key_type)
# get a delivery url
def get_delivery_url(access_token, ck_id, key_type):
    path = '/ContentKeys'
    full_path = ''.join([path, "('", ck_id, "')", "/GetKeyDeliveryUrl"])
    endpoint = ''.join([ams_rest_endpoint, full_path])
    body = '{"keyDeliveryType": "' + key_type + '"}'
    return do_ams_post(endpoint, full_path, body, access_token)

# encode_mezzanine_asset(access_token, processor_id, asset_id, output_assetname, json_profile)
# encode a mezzanine asset
def encode_mezzanine_asset(access_token, processor_id, asset_id, output_assetname, json_profile):
    path = '/Jobs'
    endpoint = ''.join([ams_rest_endpoint, path])
    assets_path = ''.join(["/Assets", "('", asset_id, "')"])
    assets_path_encoded = urllib.parse.quote(assets_path, safe='')
    endpoint_assets = ''.join([ams_rest_endpoint, assets_path_encoded])
    body = '{ \
    		"Name":"' + output_assetname + '", \
   		"InputMediaAssets":[{ \
       	  		"__metadata":{ \
       	     			"uri":"' + endpoint_assets + '" \
       	  		} \
     	 	}], \
   		"Tasks":[{ \
       	  		"Configuration":\'' + json_profile + '\', \
       	  		"MediaProcessorId":"' + processor_id + '", \
       	  		"TaskBody":"<?xml version=\\"1.0\\" encoding=\\"utf-16\\"?><taskBody><inputAsset>JobInputAsset(0)</inputAsset><outputAsset assetCreationOptions=\\"0\\" assetName=\\"' + output_assetname + '\\">JobOutputAsset(0)</outputAsset></taskBody>" \
      		}] \
	}'
    return do_ams_post(endpoint, path, body, access_token)

# validate_mp4_asset(access_token, processor_id, asset_id, output_assetname)
# validate a mp4 asset
def validate_mp4_asset(access_token, processor_id, asset_id, output_assetname):
    path = '/Jobs'
    endpoint = ''.join([ams_rest_endpoint, path])
    assets_path = ''.join(["/Assets", "('", asset_id, "')"])
    assets_path_encoded = urllib.parse.quote(assets_path, safe='')
    endpoint_assets = ''.join([ams_rest_endpoint, assets_path_encoded])
    body = '{ \
    		"Name":"ValidateEncodedMP4", \
   		"InputMediaAssets":[{ \
       	  		"__metadata":{ \
       	     			"uri":"' + endpoint_assets + '" \
       	  		} \
     	 	}], \
   		"Tasks":[{ \
       	  		"Configuration":"<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?><taskDefinition xmlns=\\"http://schemas.microsoft.com/iis/media/v4/TM/TaskDefinition#\\"><name>MP4 Preprocessor</name><id>859515BF-9BA3-4BDD-A3B6-400CEF07F870</id><description xml:lang=\\"en\\" /><inputFolder /><properties namespace=\\"http://schemas.microsoft.com/iis/media/V4/TM/MP4Preprocessor#\\" prefix=\\"mp4p\\"><property name=\\"SmoothRequired\\" value=\\"false\\" /><property name=\\"HLSRequired\\" value=\\"true\\" /></properties><taskCode><type>Microsoft.Web.Media.TransformManager.MP4PreProcessor.MP4Preprocessor_Task, Microsoft.Web.Media.TransformManager.MP4Preprocessor, Version=1.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35</type></taskCode></taskDefinition>", \
       	  		"MediaProcessorId":"' + processor_id + '", \
       	  		"TaskBody":"<?xml version=\\"1.0\\" encoding=\\"utf-16\\"?><taskBody><inputAsset>JobInputAsset(0)</inputAsset><outputAsset assetCreationOptions=\\"0\\" assetName=\\"' + output_assetname + '\\">JobOutputAsset(0)</outputAsset></taskBody>" \
      		}] \
	}'
    return do_ams_post(endpoint, path, body, access_token)

### Helpers...
# Generic functions not intended for "external" use... 
def helper_add(access_token, ck_id, path, body):
    full_path = ''.join([path, "('", ck_id, "')"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    return do_ams_put(endpoint, full_path_encoded, body, access_token, "json_only", "1.0;NetFx")

def helper_list(access_token, oid, path):
    if(oid != ""):
    	path = ''.join([path, "('", oid, "')"])
    endpoint = ''.join([ams_rest_endpoint, path])
    return do_ams_get(endpoint, path, access_token)

def helper_delete(access_token, oid, path):
    full_path = ''.join([path, "('", oid, "')"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    return do_ams_delete(endpoint, full_path_encoded, access_token)

### Aux Funcions...
# These are functions that are intended for "external" use, but are not AMS REST API's...
# Translate the numeric options/encryption of the Asset
def translate_asset_options(nr):
    if (nr == "0"): 
    	return "None"
    if (nr == "1"): 
    	return "StorageEncrypted"
    if (nr == "2"): 
    	return "CommonEncryptionProtected"
    if (nr == "4"): 
    	return "EnvelopeEncryptionProtected"

# Translate the numeric state of the Jobs
def translate_job_state(nr):
    if (nr == "0"): 
    	return "Queued"
    if (nr == "1"): 
    	return "Scheduled"
    if (nr == "2"): 
    	return "Processing"
    if (nr == "3"): 
    	return "Finished"
    if (nr == "4"): 
    	return "Error"
    if (nr == "5"): 
    	return "Canceled"
    if (nr == "6"): 
    	return "Canceling"
# Get specific url
def retrieve_url_content(url):
    return do_ams_get(endpoint, path, access_token)

### Exceptions...
# These, I think, should not be here... ;-)
# upload_block_blob(access_token, endpoint, content, content_length)
# upload a block blob
def upload_block_blob(access_token, endpoint, content, content_length):
    return do_ams_sto_put(endpoint, content, content_length, access_token)
