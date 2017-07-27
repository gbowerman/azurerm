# subnfs - place to store azurerm functions related to subscriptions
import json
import os

from .restfns import do_get
from .settings import BASE_API, get_rm_endpoint


# get_subscription_from_cli()
# get the default, or named, subscription id from CLI's local cache
# will only work if CLI local cache is present on the machine (i.e. you
# ran 'az login' once or are in Azure Cloud Shell)
def get_subscription_from_cli(name=None):
    home = os.path.expanduser('~')
    azure_profile_path = home + os.sep + '.azure' + os.sep + 'azureProfile.json'
    if os.path.isfile(azure_profile_path) is False:
        print('Error from get_subscription_from_cli(): Cannot find ' +
              azure_profile_path)
        return None
    with open(azure_profile_path, 'r') as azure_profile_fd:
        azure_profile = json.load(azure_profile_fd)
    for subscription_info in azure_profile['subscriptions']:
        if (name is None and subscription_info['isDefault'] is True) or \
                                            subscription_info['name'] == name:
            return subscription_info['id']
    return None


# list_locations(access_token, subscrpition_id)
# list available locations for a subscription
def list_locations(access_token, subscription_id):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/locations?api-version=', BASE_API])
    return do_get(endpoint, access_token)


# list_subscriptions(access_token)
# list the available Azure subscriptions for this user/service principle
def list_subscriptions(access_token):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/',
                        '?api-version=', BASE_API])
    return do_get(endpoint, access_token)
