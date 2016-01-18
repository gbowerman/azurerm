import adal
import requests

# to do: move these functions to a separate package
azure_rm_endpoint = 'https://management.azure.com/'

# do an HTTP GET request and return JSON
def do_get(endpoint, access_token):
    headers = {"Authorization": 'Bearer ' + access_token}
    return requests.get(endpoint, headers=headers).json()

# get an Azure access token using the adal library
def get_access_token(tenant_id, application_id, application_secret):
    token_response = adal.acquire_token_with_client_credentials(
        'https://login.microsoftonline.com/' + tenant_id,
        application_id,
        application_secret
    )
    return token_response.get('accessToken')

# list the available Azure subscriptions for this user/service principle
def list_subscriptions(access_token):
    api_version = '2015-01-01'
    endpoint = azure_rm_endpoint + '/subscriptions/?api-version=' + api_version
    return do_get(endpoint, access_token)


tenant_id = '72f988bf-86f1-41af-91ab-2d7cd011db47'
application_id = 'f3ea1d15-d8ff-44e7-9f75-c4d00681f6bd'
application_secret = 'SqlGuy01'

access_token = get_access_token(tenant_id, application_id, application_secret)

# list subscriptions
json_output = list_subscriptions(access_token)
for i in json_output["value"]:
    print(i["displayName"] + ': ' + i["subscriptionId"])


