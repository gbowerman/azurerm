# adalfns - place to store azurerm functions which call adal routines

import adal
from .settings import get_auth_endpoint, get_resource_endpoint

# get_access_token(tenant_id, application_id, application_secret)
# get an Azure access token using the adal library
def get_access_token(tenant_id, application_id, application_secret):
    context = adal.AuthenticationContext(get_auth_endpoint() + tenant_id, api_version = None)
    token_response = context.acquire_token_with_client_credentials(get_resource_endpoint(), application_id, \
        application_secret)
    return token_response.get('accessToken')
