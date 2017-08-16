'''azurerm restfns - REST functions for azurerm'''

import platform
import json
import pkg_resources  # to get version
import requests
from .settings import json_acceptformat, json_only_acceptformat, xml_acceptformat, batch_acceptformat, charset, dsversion_min, dsversion_max, xmsversion, \
get_rm_endpoint, ams_rest_endpoint, ams_auth_endpoint, MEDIA_API

def get_user_agent():
    '''User-Agent Header. Sends library identification to Azure endpoint.
    '''
    version = pkg_resources.require("azurerm")[0].version
    user_agent = "python/{} ({}) requests/{} azurerm/{}".format(
        platform.python_version(),
        platform.platform(),
        requests.__version__,
        version)
    return user_agent

def do_get(endpoint, access_token):
    '''Do an HTTP GET request and return JSON.

    Args:
        endpoint (str): Azure Resource Manager management endpoint.
        access_token (str): A valid Azure authentication token.

    Returns:
        HTTP response. JSON body.
    '''
    headers = {"Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    return requests.get(endpoint, headers=headers).json()


def do_get_next(endpoint, access_token):
    '''Do an HTTP GET request, follow the nextLink chain and return JSON.

    Args:
        endpoint (str): Azure Resource Manager management endpoint.
        access_token (str): A valid Azure authentication token.

    Returns:
        HTTP response. JSON body.
    '''
    headers = {"Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    looping = True
    value_list = []
    vm_dict = {}
    while looping:
        get_return = requests.get(endpoint, headers=headers).json()
        if not 'value' in get_return:
            return get_return
        if not 'nextLink' in get_return:
            looping = False
        else:
            endpoint = get_return['nextLink']
        value_list += get_return['value']
    vm_dict['value'] = value_list
    return vm_dict


def do_delete(endpoint, access_token):
    '''Do an HTTP GET request and return JSON.

    Args:
        endpoint (str): Azure Resource Manager management endpoint.
        access_token (str): A valid Azure authentication token.

    Returns:
        HTTP response.
    '''
    headers = {"Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    return requests.delete(endpoint, headers=headers)


def do_patch(endpoint, body, access_token):
    '''Do an HTTP PATCH request and return JSON.

    Args:
        endpoint (str): Azure Resource Manager management endpoint.
        body (str): JSON body of information to patch.
        access_token (str): A valid Azure authentication token.

    Returns:
        HTTP response. JSON body.
    '''
    headers = {"content-type": "application/json", "Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    return requests.patch(endpoint, data=body, headers=headers)


def do_post(endpoint, body, access_token):
    '''Do an HTTP POST request and return JSON.

    Args:
        endpoint (str): Azure Resource Manager management endpoint.
        body (str): JSON body of information to post.
        access_token (str): A valid Azure authentication token.

    Returns:
        HTTP response. JSON body.
    '''
    headers = {"content-type": "application/json", "Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    return requests.post(endpoint, data=body, headers=headers)


def do_put(endpoint, body, access_token):
    '''Do an HTTP PUT request and return JSON.

    Args:
        endpoint (str): Azure Resource Manager management endpoint.
        body (str): JSON body of information to put.
        access_token (str): A valid Azure authentication token.

    Returns:
        HTTP response. JSON body.
    '''
    headers = {"content-type": "application/json", "Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    return requests.put(endpoint, data=body, headers=headers)


''' restfns - REST functions for amspy. '''
def get_url(access_token, endpoint=ams_rest_endpoint, flag=True):
    '''Get Media Services Final Endpoint URL.
    Args:
        access_token (str): A valid Azure authentication token.
        endpoint (str): Azure Media Services Initial Endpoint.
        flag (bol): flag.

    Returns:
        HTTP response. JSON body.
    '''
    return do_ams_get_url(endpoint, access_token, flag)

# do_auth(endpoint, body, access_token)
# do an HTTP POST request for authentication (acquire an access token) and return JSON
def do_ams_auth(endpoint, body):
    headers = {"content-type": "application/x-www-form-urlencoded",
                "Accept": json_acceptformat}
    return requests.post(endpoint, data=body, headers=headers)

# do_get(endpoint, path, access_token)
# do an HTTP GET request and return JSON
def do_ams_get(endpoint, path, access_token):
    headers = {"Content-Type": json_acceptformat,
		"DataServiceVersion": dsversion_min,
		"MaxDataServiceVersion": dsversion_max,
		"Accept": json_acceptformat,
		"Accept-Charset" : charset,
		"Authorization": "Bearer " + access_token,
		"x-ms-version" : xmsversion}
    body = ''
    response = requests.get(endpoint, headers=headers, allow_redirects=False)
    # AMS response to the first call can be a redirect, 
    # so we handle it here to make it transparent for the caller...
    if (response.status_code == 301):
         redirected_url = ''.join([response.headers['location'], path])
         response = requests.get(redirected_url, data=body, headers=headers)
    return response

# do_put(endpoint, path, body, access_token, format="json", ds_min_version="3.0;NetFx")
# do an HTTP PUT request and return JSON
def do_ams_put(endpoint, path, body, access_token, format="json", ds_min_version="3.0;NetFx"):
    min_ds = dsversion_min; content_acceptformat = json_acceptformat
    if (format == "json_only"):
    	min_ds = ds_min_version
    	content_acceptformat = json_only_acceptformat
    headers = {"Content-Type": content_acceptformat,
		"DataServiceVersion": min_ds,
		"MaxDataServiceVersion": dsversion_max,
		"Accept": json_acceptformat,
		"Accept-Charset" : charset,
		"Authorization": "Bearer " + access_token,
		"x-ms-version" : xmsversion}
    response = requests.put(endpoint, data=body, headers=headers, allow_redirects=False)
    # AMS response to the first call can be a redirect, 
    # so we handle it here to make it transparent for the caller...
    if (response.status_code == 301):
    	redirected_url = ''.join([response.headers['location'], path])
    	response = requests.put(redirected_url, data=body, headers=headers)
    return response

# do_post(endpoint, body, access_token, format="json", ds_min_version="3.0;NetFx")
# do an HTTP POST request and return JSON
def do_ams_post(endpoint, path, body, access_token, format="json", ds_min_version="3.0;NetFx"):
    min_ds = dsversion_min; content_acceptformat = json_acceptformat; acceptformat = json_acceptformat
    if (format == "json_only"):
    	min_ds = ds_min_version
    	content_acceptformat = json_only_acceptformat
    if (format == "xml"):
    	content_acceptformat = xml_acceptformat
    	acceptformat = xml_acceptformat + ",application/xml" 
    headers = {"Content-Type": content_acceptformat, 
		"DataServiceVersion": min_ds,
		"MaxDataServiceVersion": dsversion_max,
		"Accept": acceptformat,
		"Accept-Charset" : charset,
		"Authorization": "Bearer " + access_token,
		"x-ms-version" : xmsversion}
    response = requests.post(endpoint, data=body, headers=headers, allow_redirects=False)
    # AMS response to the first call can be a redirect, 
    # so we handle it here to make it transparent for the caller...
    if (response.status_code == 301):
         redirected_url = ''.join([response.headers['location'], path])
         response = requests.post(redirected_url, data=body, headers=headers)
    return response

# do_patch(endpoint, path, body, access_token)
# do an HTTP PATCH request and return JSON
def do_ams_patch(endpoint, path, body, access_token):
    headers = {"Content-Type": json_acceptformat, 
		"DataServiceVersion": dsversion_min,
		"MaxDataServiceVersion": dsversion_max,
		"Accept": json_acceptformat,
		"Accept-Charset" : charset,
		"Authorization": "Bearer " + access_token,
		"x-ms-version" : xmsversion}
    response = requests.patch(endpoint, data=body, headers=headers, allow_redirects=False)
    # AMS response to the first call can be a redirect, 
    # so we handle it here to make it transparent for the caller...
    if (response.status_code == 301):
         redirected_url = ''.join([response.headers['location'], path])
         response = requests.patch(redirected_url, data=body, headers=headers)
    return response

# do_delete(endpoint, access_token)
# do an HTTP DELETE request and return JSON
def do_ams_delete(endpoint, path, access_token):
    headers = {"DataServiceVersion": dsversion_min,
		"MaxDataServiceVersion": dsversion_max,
		"Accept": json_acceptformat,
		"Accept-Charset" : charset,
		"Authorization": 'Bearer ' + access_token,
		"x-ms-version" : xmsversion}
    response = requests.delete(endpoint, headers=headers, allow_redirects=False)
    # AMS response to the first call can be a redirect, 
    # so we handle it here to make it transparent for the caller...
    if (response.status_code == 301):
         redirected_url = ''.join([response.headers['location'], path])
         response = requests.delete(redirected_url, headers=headers)
    return response

# do_sto_put(endpoint, body, access_token)
# do an HTTP PUT request to the azure storage api and return JSON
def do_ams_sto_put(endpoint, body, content_length, access_token):
    headers = {"Accept": json_acceptformat,
		"Accept-Charset" : charset,
		"x-ms-blob-type" : "BlockBlob",
		"x-ms-meta-m1": "v1",
		"x-ms-meta-m2": "v2",
		"x-ms-version" : "2015-02-21",
		"Content-Length" : str(content_length)}
    return requests.put(endpoint, data=body, headers=headers)

# do_ams_get_url(endpoint, access_token)
# do an HTTP GET request and return JSON
def do_ams_get_url(endpoint, access_token, flag=True):
    headers = {"Content-Type": json_acceptformat,
		"DataServiceVersion": dsversion_min,
		"MaxDataServiceVersion": dsversion_max,
		"Accept": json_acceptformat,
		"Accept-Charset" : charset,
		"Authorization": "Bearer " + access_token,
		"x-ms-version" : xmsversion}
    body = ''
    response = requests.get(endpoint, headers=headers, allow_redirects=flag)
    if(flag):
    	if (response.status_code == 301):
    		response = requests.get(response.headers['location'], data=body, headers=headers)
    return response
