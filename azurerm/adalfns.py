#!/usr/bin/env python

"""
Copyright (c) 2016, Guy Bowerman
Description: Azure Resource Manager Python library
License: MIT (see LICENSE.txt file for details)
"""

# adalfns - place to store azurerm functions which call adal routines

import adal

authentication_endpoint = 'https://login.microsoftonline.com/'

# get_access_token(tenant_id, application_id, application_secret)
# get an Azure access token using the adal library
def get_access_token(tenant_id, application_id, application_secret):
    token_response = adal.acquire_token_with_client_credentials(
        authentication_endpoint + tenant_id,
        application_id,
        application_secret
    )
    return token_response.get('accessToken')