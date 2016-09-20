# insightsrp.py - azurerm functions for the Microsoft.Insights resource provider

from .restfns import do_get
from .settings import azure_rm_endpoint, INSIGHTS_API, INSIGHTS_PREVIEW_API

# list_autoscale_settings(access_token, subscription_id)
# list the autoscale settings in a subscription_id
def list_autoscale_settings(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/microsoft.insights/',
                        '/autoscaleSettings?api-version=', INSIGHTS_API])
    return do_get(endpoint, access_token)


# list_insights_components(access_token, subscription_id, resource_group)
# list the Microsoft Insights components in a resource group	
def list_insights_components(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/microsoft.insights/',
                        '/components?api-version=', INSIGHTS_API])
    return do_get(endpoint, access_token)

# list_metric_definitions_for_resource(access_token, subscription_id, resource_group, resource_provider, resource_type, resource_name)
# list the monitoring metric definitions for a resource
def list_metric_definitions_for_resource(access_token, subscription_id, resource_group, resource_provider, resource_type, resource_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/', resource_provider,
                        '/', resource_type,
                        '/', resource_name,
                        '/providers/microsoft.insights',
                        '/metricdefinitions?api-version=', INSIGHTS_API])
    return do_get(endpoint, access_token)


# get_metrics_for_resource(access_token, subscription_id, resource_group, resource_provider, resource_type, resource_name)
# get the monitoring metrics for a resource
def get_metrics_for_resource(access_token, subscription_id, resource_group, resource_provider, resource_type, resource_name):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/', resource_provider,
                        '/', resource_type,
                        '/', resource_name,
                        '/providers/microsoft.insights/',
                        '/metrics?api-version=', INSIGHTS_PREVIEW_API])
    return do_get(endpoint, access_token)
