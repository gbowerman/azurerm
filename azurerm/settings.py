# settings.py - place to store constants for azurerm
import os

azure_rm_endpoint = 'https://management.azure.com'

ACS_API = '2017-01-31'
BASE_API = '2016-09-01'
COMP_API = '2017-03-30'
INSIGHTS_API = '2015-04-01'
INSIGHTS_METRICS_API = '2016-03-01'
INSIGHTS_PREVIEW_API = '2016-06-01'
MEDIA_API = '2015-10-01'
NETWORK_API = '2017-04-01'
STORAGE_API = '2016-01-01'

# Isolated cloud support..
# allow Azure endpoints to bet set by environment variable, else return default values
def get_rm_endpoint():
    rm_endpoint = os.environ.get('AZURE_RM_ENDPOINT')
    if rm_endpoint is None:
        return azure_rm_endpoint
    else:
        return rm_endpoint

