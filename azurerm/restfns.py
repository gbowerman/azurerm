# restfns - REST functions for azurerm

import requests


# import json

# do_get(endpoint, access_token)
# do an HTTP GET request and return JSON
def do_get(endpoint, access_token):
    headers = {"Authorization": 'Bearer ' + access_token}
    return requests.get(endpoint, headers=headers).json()


# do_get_next(endpoint, access_token)
# do an HTTP GET request, follow the nextLink chain and return JSON
def do_get_next(endpoint, access_token):
    headers = {"Authorization": 'Bearer ' + access_token}
    looping = True
    value_list = []
    vm_dict = {}
    while(looping):
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


# do_delete(endpoint, access_token)
# do an HTTP GET request and return JSON
def do_delete(endpoint, access_token):
    headers = {"Authorization": 'Bearer ' + access_token}
    return requests.delete(endpoint, headers=headers)


# do_patch(endpoint, body, access_token)
# do an HTTP PATCH request and return JSON
def do_patch(endpoint, body, access_token):
    headers = {"content-type": "application/json", "Authorization": 'Bearer ' + access_token}
    return requests.patch(endpoint, data=body, headers=headers)


# do_post(endpoint, body, access_token)
# do an HTTP POST request and return JSON
def do_post(endpoint, body, access_token):
    headers = {"content-type": "application/json", "Authorization": 'Bearer ' + access_token}
    return requests.post(endpoint, data=body, headers=headers)


# do_put(endpoint, body, access_token)
# do an HTTP PUT request and return JSON
def do_put(endpoint, body, access_token):
    headers = {"content-type": "application/json", "Authorization": 'Bearer ' + access_token}
    return requests.put(endpoint, data=body, headers=headers)