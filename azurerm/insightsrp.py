'''insightsrp.py - azurerm functions for the Microsoft.Insights resource provider'''
import json
from .restfns import do_get, do_put
from .settings import get_rm_endpoint, INSIGHTS_API, INSIGHTS_METRICS_API, INSIGHTS_PREVIEW_API


def create_autoscale_rule(subscription_id, resource_group, vmss_name, metric_name, operator,
                          threshold, direction, change_count, time_grain='PT1M',
                          time_window='PT5M', cool_down='PT1M'):
    '''Create a new autoscale rule - pass the output in a list to create_autoscale_setting().
    '''
    metric_trigger = {'metricName': metric_name}
    metric_trigger['metricNamespace'] = ''
    metric_trigger['metricResourceUri'] = '/subscriptions/' + subscription_id + \
        '/resourceGroups/' + resource_group + \
        '/providers/Microsoft.Compute/virtualMachineScaleSets/' + vmss_name
    metric_trigger['timeGrain'] = time_grain
    metric_trigger['statistic'] = 'Average'
    metric_trigger['timeWindow'] = time_window
    metric_trigger['timeAggregation'] = 'Average'
    metric_trigger['operator'] = operator
    metric_trigger['threshold'] = threshold
    scale_action = {'direction': direction}
    scale_action['type'] = 'ChangeCount'
    scale_action['value'] = str(change_count)
    scale_action['cooldown'] = cool_down
    new_rule = {'metricTrigger': metric_trigger}
    new_rule['scaleAction'] = scale_action
    return new_rule


def create_autoscale_setting(access_token, subscription_id, resource_group, setting_name,
                             vmss_name, location, minval, maxval, default, autoscale_rules,
                             notify=None):
    '''Create a new autoscale setting for a scale set.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/microsoft.insights/autoscaleSettings/', setting_name,
                        '?api-version=', INSIGHTS_API])
    autoscale_setting = {'location': location}
    profile = {'name': 'Profile1'}
    capacity = {'minimum': str(minval)}
    capacity['maximum'] = str(maxval)
    capacity['default'] = str(default)
    profile['capacity'] = capacity
    profile['rules'] = autoscale_rules
    profiles = [profile]
    properties = {'name': setting_name}
    properties['profiles'] = profiles
    properties['targetResourceUri'] = '/subscriptions/' + subscription_id + \
        '/resourceGroups/' + resource_group + \
        '/providers/Microsoft.Compute/virtualMachineScaleSets/' + vmss_name
    properties['enabled'] = True
    if notify is not None:
        notification = {'operation': 'Scale'}
        email = {'sendToSubscriptionAdministrato': False}
        email['sendToSubscriptionCoAdministrators'] = False
        email['customEmails'] = [notify]
        notification = {'email': email}
        properties['notifications'] = [notification]
    autoscale_setting['properties'] = properties
    body = json.dumps(autoscale_setting)
    return do_put(endpoint, body, access_token)


def list_autoscale_settings(access_token, subscription_id):
    '''List the autoscale settings in a subscription_id.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/microsoft.insights/',
                        '/autoscaleSettings?api-version=', INSIGHTS_API])
    return do_get(endpoint, access_token)


def list_insights_components(access_token, subscription_id, resource_group):
    '''List the Microsoft Insights components in a resource group.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/microsoft.insights/',
                        '/components?api-version=', INSIGHTS_API])
    return do_get(endpoint, access_token)


def list_metric_defs_for_resource(access_token, subscription_id, resource_group,
                                  resource_provider, resource_type, resource_name):
    '''List the monitoring metric definitions for a resource.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/', resource_provider,
                        '/', resource_type,
                        '/', resource_name,
                        '/providers/microsoft.insights',
                        '/metricdefinitions?api-version=', INSIGHTS_METRICS_API])
    return do_get(endpoint, access_token)


def get_metrics_for_resource(access_token, subscription_id, resource_group, resource_provider,
                             resource_type, resource_name):
    '''Get the monitoring metrics for a resource.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/', resource_provider,
                        '/', resource_type,
                        '/', resource_name,
                        '/providers/microsoft.insights',
                        '/metrics?api-version=', INSIGHTS_PREVIEW_API])
    return do_get(endpoint, access_token)


def get_events_for_subscription(access_token, subscription_id, start_timestamp):
    '''Get the insights evens for a subsctipion since the specific timestamp.
    
    Example start_timetamp value: '2017-05-01T00:00:00.0000000Z'.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/providers/microsoft.insights/eventtypes/management/values?api-version=',
                        INSIGHTS_API, '&$filter=eventTimestamp ge \'', start_timestamp, '\''])
    return do_get(endpoint, access_token)
