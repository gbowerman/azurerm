''' amspy - library for easy Azure Media Services calls from Python. '''

from .amsrp import get_ams_access_token, create_media_asset, list_media_asset, create_media_assetfile, \
	list_content_key, list_asset_accesspolicy, create_asset_accesspolicy, create_sas_locator, \
	list_sas_locator, list_media_job, list_media_processor, upload_block_blob, update_media_assetfile, \
	delete_sas_locator, delete_asset_accesspolicy, delete_content_key, create_media_job, \
	delete_media_asset, validate_mp4_asset, translate_job_state, translate_asset_options, link_asset_content_key, \
	get_url, create_contentkey_authorization_policy, create_contentkey_authorization_policy_options, \
	link_contentkey_authorization_policy, add_authorization_policy, get_delivery_url, create_asset_delivery_policy, \
	link_asset_delivery_policy, create_ondemand_streaming_locator, list_contentkey_authorization_policy, \
	list_contentkey_authorization_policy_options, list_streaming_endpoint, delete_contentkey_authorization_policy, \
	delete_contentkey_authorization_policy_options, list_asset_delivery_policy, delete_asset_delivery_policy, \
	create_streaming_endpoint, scale_streaming_endpoint, delete_streaming_endpoint, encode_mezzanine_asset
