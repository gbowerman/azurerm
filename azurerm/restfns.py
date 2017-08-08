'''azurerm restfns - REST functions for azurerm'''
import platform

import pkg_resources  # to get version
import requests


def get_user_agent():
    '''User-Agent Header.
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
    '''
    headers = {"Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    return requests.get(endpoint, headers=headers).json()


def do_get_next(endpoint, access_token):
    '''Do an HTTP GET request, follow the nextLink chain and return JSON.
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
    '''
    headers = {"Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    return requests.delete(endpoint, headers=headers)


def do_patch(endpoint, body, access_token):
    '''Do an HTTP PATCH request and return JSON.
    '''
    headers = {"content-type": "application/json", "Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    return requests.patch(endpoint, data=body, headers=headers)


def do_post(endpoint, body, access_token):
    '''Do an HTTP POST request and return JSON.
    '''
    headers = {"content-type": "application/json", "Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    return requests.post(endpoint, data=body, headers=headers)


def do_put(endpoint, body, access_token):
    '''Do an HTTP PUT request and return JSON.
    '''
    headers = {"content-type": "application/json", "Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    return requests.put(endpoint, data=body, headers=headers)
