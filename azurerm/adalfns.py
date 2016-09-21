# adalfns - place to store azurerm functions which call adal routines

import adal

# get_access_token(tenant_id, application_id, application_secret)
# get an Azure access token using the adal library
def get_access_token(tenant_id, application_id, application_secret, \
        authentication_endpoint='https://login.microsoftonline.com/', \
        resource='https://management.core.windows.net/'):
    context = adal.AuthenticationContext(authentication_endpoint + tenant_id)
    token_response = context.acquire_token_with_client_credentials(resource, application_id, \
        application_secret)
    return token_response.get('accessToken')
