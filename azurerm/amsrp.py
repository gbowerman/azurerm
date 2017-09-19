'''amsrp.py - azurerm functions for the Microsoft.Media resource provider and AMS Rest Interface.'''

import json
import urllib
from .restfns import do_get, do_put, do_post, do_delete, do_ams_auth, do_ams_get, \
do_ams_post, do_ams_put, do_ams_delete, do_ams_patch, do_ams_sto_put
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
    return do_post(endpoint, body, access_token)


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
    return do_put(endpoint, body, access_token)


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
    return do_delete(endpoint, access_token)


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
    return do_get(endpoint, access_token)


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
    return do_get(endpoint, access_token)


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
    return do_get(endpoint, access_token)


def get_ams_access_token(accountname, accountkey):
    '''Get Media Services Authentication Token.

    Args:
        accountname (str): Azure Media Services account name.
        accountkey (str): Azure Media Services Key.

    Returns:
        HTTP response. JSON body.
    '''
    accountkey_encoded = urllib.parse.quote(accountkey, safe='')
    body = "grant_type=client_credentials&client_id=" + accountname + \
	"&client_secret=" + accountkey_encoded + " &scope=urn%3aWindowsAzureMediaServices"
    return do_ams_auth(ams_auth_endpoint, body)


def list_media_asset(access_token, oid=""):
    '''List Media Service Asset(s).

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Asset OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/Assets'
    return helper_list(access_token, oid, path)


def list_content_key(access_token, oid=""):
    '''List Media Service Content Key(s).

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Content Key OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/ContentKeys'
    return helper_list(access_token, oid, path)


def list_contentkey_authorization_policy(access_token, oid=""):
    '''List Media Service Content Key Authorization Policy(ies).

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Content Key Authorization Policy OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/ContentKeyAuthorizationPolicies'
    return helper_list(access_token, oid, path)


def list_contentkey_authorization_policy_options(access_token, oid=""):
    '''List Media Service Content Key Authorization Policy Option(s).

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Content Key Authorization Policy Option OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/ContentKeyAuthorizationPolicyOptions'
    return helper_list(access_token, oid, path)


def list_media_processor(access_token, oid=""):
    '''List Media Service Processor(s).

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Processor OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/MediaProcessors'
    return helper_list(access_token, oid, path)


def list_asset_accesspolicy(access_token, oid=""):
    '''List Media Service Asset Access Policy(ies).

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Asset Access Policy OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/AccessPolicies'
    return helper_list(access_token, oid, path)


def list_sas_locator(access_token, oid=""):
    '''List Media Service SAS Locator(s).

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service SAS Locator OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/Locators'
    return helper_list(access_token, oid, path)


def list_media_job(access_token, oid=""):
    '''List Media Service Job(s).

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Job OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/Jobs'
    return helper_list(access_token, oid, path)


def list_asset_delivery_policy(access_token, oid=""):
    '''List Media Service Asset Delivery Policy(ies).

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Asset Delivery Policy OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/AssetDeliveryPolicies'
    return helper_list(access_token, oid, path)


def list_streaming_endpoint(access_token, oid=""):
    '''List Media Service Streaming Endpoint(s).

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Streaming Endpoint OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/StreamingEndpoints'
    return helper_list(access_token, oid, path)


def delete_streaming_endpoint(access_token, oid):
    '''Delete Media Service Streaming Endpoint.

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Streaming Endpoint OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/StreamingEndpoints'
    return helper_delete(access_token, oid, path)


def delete_asset_delivery_policy(access_token, oid):
    '''Delete Media Service Asset Delivery Policy.

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Delivery Policy OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/AssetDeliveryPolicies'
    return helper_delete(access_token, oid, path)


def delete_asset_accesspolicy(access_token, oid):
    '''Delete Media Service Asset Access Policy.

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Asset Access Policy OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/AccessPolicies'
    return helper_delete(access_token, oid, path)


def delete_sas_locator(access_token, oid):
    '''Delete Media Service SAS Locator.

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service SAS Locator OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/Locators'
    return helper_delete(access_token, oid, path)


def delete_content_key(access_token, oid):
    '''Delete Media Service Content Key.

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Content Key OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/ContentKeys'
    return helper_delete(access_token, oid, path)


def delete_contentkey_authorization_policy(access_token, oid):
    '''Delete Media Service Content Key Authorization Policy.

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Content Key Authorization Policy OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/ContentKeyAuthorizationPolicies'
    return helper_delete(access_token, oid, path)


def delete_contentkey_authorization_policy_options(access_token, oid):
    '''Delete Media Service Content Key Authorization Policy Option.

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Content Key Authorization Policy Option OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/ContentKeyAuthorizationPolicyOptions'
    return helper_delete(access_token, oid, path)


def delete_media_asset(access_token, oid):
    '''Delete Media Service Media Asset.

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): Media Service Asset OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/Assets'
    return helper_delete(access_token, oid, path)


def create_media_asset(access_token, name, options="0"):
    '''Create Media Service Asset.

    Args:
        access_token (str): A valid Azure authentication token.
        name (str): Media Service Asset Name.
        options (str): Media Service Options.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/Assets'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = '{"Name": "' + name + '", "Options": "' + str(options) + '"}'
    return do_ams_post(endpoint, path, body, access_token)


def create_media_assetfile(access_token, parent_asset_id, name, is_primary="false", \
is_encrypted="false", encryption_scheme="None", encryptionkey_id="None"):
    '''Create Media Service Asset File.

    Args:
        access_token (str): A valid Azure authentication token.
        parent_asset_id (str): Media Service Parent Asset ID.
        name (str): Media Service Asset Name.
        is_primary (str): Media Service Primary Flag.
        is_encrypted (str): Media Service Encryption Flag.
        encryption_scheme (str): Media Service Encryption Scheme.
        encryptionkey_id (str): Media Service Encryption Key ID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/Files'
    endpoint = ''.join([ams_rest_endpoint, path])
    if encryption_scheme == "StorageEncryption":
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


def create_sas_locator(access_token, asset_id, accesspolicy_id):
    '''Create Media Service SAS Locator.

    Args:
        access_token (str): A valid Azure authentication token.
        asset_id (str): Media Service Asset ID.
        accesspolicy_id (str): Media Service Access Policy ID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/Locators'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = '{ \
		"AccessPolicyId":"' + accesspolicy_id + '", \
		"AssetId":"' + asset_id + '", \
		"Type":1 \
	}'
    return do_ams_post(endpoint, path, body, access_token)


def create_asset_delivery_policy(access_token, ams_account, key_delivery_url):
    '''Create Media Service Asset Delivery Policy.

    Args:
        access_token (str): A valid Azure authentication token.
        ams_account (str): Media Service Account.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/AssetDeliveryPolicies'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = '{ \
		"Name":"AssetDeliveryPolicy", \
		"AssetDeliveryProtocol":"4", \
		"AssetDeliveryPolicyType":"3", \
		"AssetDeliveryConfiguration":"[{ \
			\\"Key\\":\\"2\\", \
			\\"Value\\":\\"' + key_delivery_url + '\\"}]" \
	}'
    return do_ams_post(endpoint, path, body, access_token)


def create_contentkey_authorization_policy(access_token, content):
    '''Create Media Service Content Key Authorization Policy.

    Args:
        access_token (str): A valid Azure authentication token.
        content (str): Content Payload.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/ContentKeyAuthorizationPolicies'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = content
    return do_ams_post(endpoint, path, body, access_token)


def create_contentkey_authorization_policy_options(access_token, key_delivery_type="2", \
name="HLS Open Authorization Policy", key_restriction_type="0"):
    '''Create Media Service Content Key Authorization Policy Options.

    Args:
        access_token (str): A valid Azure authentication token.
        key_delivery_type (str): A Media Service Content Key Authorization Policy Delivery Type.
        name (str): A Media Service Contenty Key Authorization Policy Name.
        key_restiction_type (str): A Media Service Contenty Key Restriction Type.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/ContentKeyAuthorizationPolicyOptions'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = '{ \
		"Name":"policy",\
		"KeyDeliveryType":"' + key_delivery_type + '", \
		"KeyDeliveryConfiguration":"", \
			"Restrictions":[{ \
			"Name":"' + name + '", \
			"KeyRestrictionType":"' + key_restriction_type + '", \
			"Requirements":null \
		}] \
	}'
    return do_ams_post(endpoint, path, body, access_token, "json_only")


def create_ondemand_streaming_locator(access_token, encoded_asset_id, pid, starttime=None):
    '''Create Media Service OnDemand Streaming Locator.

    Args:
        access_token (str): A valid Azure authentication token.
        encoded_asset_id (str): A Media Service Encoded Asset ID.
        pid (str): A Media Service Encoded PID.
        starttime (str): A Media Service Starttime.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/Locators'
    endpoint = ''.join([ams_rest_endpoint, path])
    if starttime is None:
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


def create_asset_accesspolicy(access_token, name, duration, permission="1"):
    '''Create Media Service Asset Access Policy.

    Args:
        access_token (str): A valid Azure authentication token.
        name (str): A Media Service Asset Access Policy Name.
        duration (str): A Media Service duration.
        permission (str): A Media Service permission.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/AccessPolicies'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = '{ \
		"Name": "' + str(name) + '", \
		"DurationInMinutes": "' + duration + '", \
		"Permissions": "' + permission + '" \
	}'
    return do_ams_post(endpoint, path, body, access_token)


def create_streaming_endpoint(access_token, name, description="New Streaming Endpoint", \
scale_units="1"):
    '''Create Media Service Streaming Endpoint.

    Args:
        access_token (str): A valid Azure authentication token.
        name (str): A Media Service Streaming Endpoint Name.
        description (str): A Media Service Streaming Endpoint Description.
        scale_units (str): A Media Service Scale Units Number.

    Returns:
        HTTP response. JSON body.
    '''
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


def scale_streaming_endpoint(access_token, streaming_endpoint_id, scale_units):
    '''Scale Media Service Streaming Endpoint.

    Args:
        access_token (str): A valid Azure authentication token.
        streaming_endpoint_id (str): A Media Service Streaming Endpoint ID.
        scale_units (str): A Media Service Scale Units Number.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/StreamingEndpoints'
    full_path = ''.join([path, "('", streaming_endpoint_id, "')", "/Scale"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    body = '{"scaleUnits": "' + str(scale_units) + '"}'
    return do_ams_post(endpoint, full_path_encoded, body, access_token)


def link_asset_content_key(access_token, asset_id, encryptionkey_id, ams_redirected_rest_endpoint):
    '''Link Media Service Asset and Content Key.

    Args:
        access_token (str): A valid Azure authentication token.
        asset_id (str): A Media Service Asset ID.
        encryption_id (str): A Media Service Encryption ID.
        ams_redirected_rest_endpoint (str): A Media Service Redirected Endpoint.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/Assets'
    full_path = ''.join([path, "('", asset_id, "')", "/$links/ContentKeys"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    uri = ''.join([ams_redirected_rest_endpoint, 'ContentKeys', "('", encryptionkey_id, "')"])
    body = '{"uri": "' + uri + '"}'
    return do_ams_post(endpoint, full_path_encoded, body, access_token)


def link_asset_delivery_policy(access_token, asset_id, adp_id, ams_redirected_rest_endpoint):
    '''Link Media Service Asset Delivery Policy.

    Args:
        access_token (str): A valid Azure authentication token.
        asset_id (str): A Media Service Asset ID.
        adp_id (str): A Media Service Asset Delivery Policy ID.
        ams_redirected_rest_endpoint (str): A Media Service Redirected Endpoint.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/Assets'
    full_path = ''.join([path, "('", asset_id, "')", "/$links/DeliveryPolicies"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    uri = ''.join([ams_redirected_rest_endpoint, 'AssetDeliveryPolicies', "('", adp_id, "')"])
    body = '{"uri": "' + uri + '"}'
    return do_ams_post(endpoint, full_path_encoded, body, access_token)


def link_contentkey_authorization_policy(access_token, ckap_id, options_id, \
ams_redirected_rest_endpoint):
    '''Link Media Service Content Key Authorization Policy.

    Args:
        access_token (str): A valid Azure authentication token.
        ckap_id (str): A Media Service Asset Content Key Authorization Policy ID.
        options_id (str): A Media Service Content Key Authorization Policy Options .
        ams_redirected_rest_endpoint (str): A Media Service Redirected Endpoint.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/ContentKeyAuthorizationPolicies'
    full_path = ''.join([path, "('", ckap_id, "')", "/$links/Options"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    uri = ''.join([ams_redirected_rest_endpoint, 'ContentKeyAuthorizationPolicyOptions', \
    "('", options_id, "')"])
    body = '{"uri": "' + uri + '"}'
    return do_ams_post(endpoint, full_path_encoded, body, access_token, "json_only", "1.0;NetFx")


def add_authorization_policy(access_token, ck_id, oid):
    '''Add Media Service Authorization Policy.

    Args:
        access_token (str): A valid Azure authentication token.
        ck_id (str): A Media Service Asset Content Key ID.
        options_id (str): A Media Service OID.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/ContentKeys'
    body = '{"AuthorizationPolicyId":"' + oid + '"}'
    return helper_add(access_token, ck_id, path, body)


def update_media_assetfile(access_token, parent_asset_id, asset_id, content_length, name):
    '''Update Media Service Asset File.

    Args:
        access_token (str): A valid Azure authentication token.
        parent_asset_id (str): A Media Service Asset Parent Asset ID.
        asset_id (str): A Media Service Asset Asset ID.
        content_length (str): A Media Service Asset Content Length.
        name (str): A Media Service Asset name.

    Returns:
        HTTP response. JSON body.
    '''
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


def get_key_delivery_url(access_token, ck_id, key_type):
    '''Get Media Services Key Delivery URL.

    Args:
        access_token (str): A valid Azure authentication token.
        ck_id (str): A Media Service Content Key ID.
        key_type (str): A Media Service key Type.

    Returns:
        HTTP response. JSON body.
    '''
    path = '/ContentKeys'
    full_path = ''.join([path, "('", ck_id, "')", "/GetKeyDeliveryUrl"])
    endpoint = ''.join([ams_rest_endpoint, full_path])
    body = '{"keyDeliveryType": "' + key_type + '"}'
    return do_ams_post(endpoint, full_path, body, access_token)


def encode_mezzanine_asset(access_token, processor_id, asset_id, output_assetname, json_profile):
    '''Get Media Service Encode Mezanine Asset.

    Args:
        access_token (str): A valid Azure authentication token.
        processor_id (str): A Media Service Processor ID.
        asset_id (str): A Media Service Asset ID.
        output_assetname (str): A Media Service Asset Name.
        json_profile (str): A Media Service JSON Profile.

    Returns:
        HTTP response. JSON body.
    '''
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


def validate_mp4_asset(access_token, processor_id, asset_id, output_assetname):
    '''Validate MP4 File.

    Args:
        access_token (str): A valid Azure authentication token.
        processor_id (str): A Media Service Processor ID.
        asset_id (str): A Media Service Asset ID.
        output_assetname (str): A Media Service Asset Name.

    Returns:
        HTTP response. JSON body.
    '''
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


def helper_add(access_token, ck_id, path, body):
    '''Helper Function to add strings to a URL path.

    Args:
        access_token (str): A valid Azure authentication token.
        ck_id (str): A CK ID.
        path (str): A URL Path.
        body (str): A Body.

    Returns:
        HTTP response. JSON body.
    '''
    full_path = ''.join([path, "('", ck_id, "')"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    return do_ams_put(endpoint, full_path_encoded, body, access_token, "json_only", "1.0;NetFx")


def helper_list(access_token, oid, path):
    '''Helper Function to list a URL path.

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): An OID.
        path (str): A URL Path.

    Returns:
        HTTP response. JSON body.
    '''
    if oid != "":
        path = ''.join([path, "('", oid, "')"])
    endpoint = ''.join([ams_rest_endpoint, path])
    return do_ams_get(endpoint, path, access_token)


def helper_delete(access_token, oid, path):
    '''Helper Function to delete a Object at a URL path.

    Args:
        access_token (str): A valid Azure authentication token.
        oid (str): An OID.
        path (str): A URL Path.

    Returns:
        HTTP response. JSON body.
    '''
    full_path = ''.join([path, "('", oid, "')"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    return do_ams_delete(endpoint, full_path_encoded, access_token)


def translate_asset_options(code):
    '''AUX Function to translate the asset (numeric) encryption option of an Asset.

    Args:
        nr (int): A valid number to translate.

    Returns:
        HTTP response. JSON body.
    '''
    if code == "0":
        return "None"
    if code == "1":
        return "StorageEncrypted"
    if code == "2":
        return "CommonEncryptionProtected"
    if code == "4":
        return "EnvelopeEncryptionProtected"


def translate_job_state(code):
    '''AUX Function to translate the (numeric) state of a Job.

    Args:
        nr (int): A valid number to translate.

    Returns:
        HTTP response. JSON body.
    '''
    code_description = ""
    if code == "0":
        code_description = "Queued"
    if code == "1":
        code_description = "Scheduled"
    if code == "2":
        code_description = "Processing"
    if code == "3":
        code_description = "Finished"
    if code == "4":
        code_description = "Error"
    if code == "5":
        code_description = "Canceled"
    if code == "6":
        code_description = "Canceling"

    return code_description


### Exceptions...
# These, I think, should not be here... ;-)
# upload_block_blob(access_token, endpoint, content, content_length)
# upload a block blob
def upload_block_blob(endpoint, content, content_length):
    '''AUX (quick and dirty) Function to upload a block Blob..

    Args:
        access_token (str): A valid Azure authentication token.
        endpoint (str): A Media Service Endpoint.
        content (str): A Content.
        content_length (str): A Content Length.

    Returns:
        HTTP response. JSON body.
    '''
    return do_ams_sto_put(endpoint, content, content_length)
