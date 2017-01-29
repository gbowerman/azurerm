# azurerm restfns - REST functions for azurerm
import json
import requests
import pkg_resources # to get version
import platform 

# User-Agent Header
def get_user_agent():
    version = pkg_resources.require("azurerm")[0].version
    user_agent = "python/{} ({}) requests/{} azurerm/{}".format(
        platform.python_version(),
        platform.platform(),
        requests.__version__,
        version)
    return user_agent

# do_get(endpoint, access_token)
# do an HTTP GET request and return JSON
def do_get(endpoint, access_token):
    headers = {"Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    return requests.get(endpoint, headers=headers).json()


# do_get_next(endpoint, access_token)
# do an HTTP GET request, follow the nextLink chain and return JSON
def do_get_next(endpoint, access_token):
    headers = {"Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    looping = True
    value_list = []
    vm_dict = {}
    while(looping):
        get_return = requests.get(endpoint, headers=headers).json()
        # print(json.dumps(get_return[get_return, sort_keys=False, indent=2, separators=(',', ': ')))
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
    headers['User-Agent'] = get_user_agent()
    return requests.delete(endpoint, headers=headers)


# do_patch(endpoint, body, access_token)
# do an HTTP PATCH request and return JSON
def do_patch(endpoint, body, access_token):
    headers = {"content-type": "application/json", "Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    return requests.patch(endpoint, data=body, headers=headers)


# do_post(endpoint, body, access_token)
# do an HTTP POST request and return JSON
def do_post(endpoint, body, access_token):
    headers = {"content-type": "application/json", "Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    return requests.post(endpoint, data=body, headers=headers)


# do_put(endpoint, body, access_token)
# do an HTTP PUT request and return JSON
def do_put(endpoint, body, access_token):
    headers = {"content-type": "application/json", "Authorization": 'Bearer ' + access_token}
    headers['User-Agent'] = get_user_agent()
    return requests.put(endpoint, data=body, headers=headers)