# restfns - REST functions for azurerm

import requests

# do_get(endpoint, access_token)
# do an HTTP GET request and return JSON
def do_get(endpoint, access_token):
    headers = {"Authorization": 'Bearer ' + access_token}
    return requests.get(endpoint, headers=headers).json()

# do_delete(endpoint, access_token)
# do an HTTP GET request and return JSON
def do_delete(endpoint, access_token):
    headers = {"Authorization": 'Bearer ' + access_token}
    return requests.delete(endpoint, headers=headers)

# do_put(endpoint, body, access_token)
# do an HTTP PUT request and return JSON
def do_put(endpoint, body, access_token):
    headers = {"content-type": "application/json", "Authorization": 'Bearer ' + access_token}
    return requests.put(endpoint, data=body, headers=headers)
	
# do_post(endpoint, body, access_token)
# do an HTTP POST request and return JSON
def do_post(endpoint, body, access_token):
    headers = {"content-type": "application/json", "Authorization": 'Bearer ' + access_token}
    return requests.post(endpoint, data=body, headers=headers)