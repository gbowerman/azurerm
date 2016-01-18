# subnfs - place to store azurerm functions related to subscriptions

from .settings import azure_rm_endpoint, BASEAPI
from .restfns import do_get

# list_subscriptions(access_token)
# list the available Azure subscriptions for this user/service principle
def list_subscriptions(access_token):
    endpoint = ''.join([azure_rm_endpoint, 
	                    '/subscriptions/', 
			            '?api-version=', BASEAPI]) 
    return do_get(endpoint, access_token)