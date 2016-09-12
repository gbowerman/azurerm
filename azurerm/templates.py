# templates.py - azurerm functions for deploying templates

from .restfns import do_put
from .settings import azure_rm_endpoint, BASE_API


# deploy_template(access_token, subscription_id, resource_group, deployment_name, template, parameters)
# deploy a template referenced by a JSON string, with parameters as a JSON string
def deploy_template(access_token, subscription_id, resource_group, deployment_name, template, parameters):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.Resources/deployments/', deployment_name,
                        '?api-version=', BASE_API])
    body = ''.join(['{   "properties": {     "template": ', template,
                    ',     "mode": "Incremental",',
                    '     "parameters": ', parameters,
                    '}}'])

    return do_put(endpoint, body, access_token)


# deploy_template_uri(access_token, subscription_id, resource_group, deployment_name, template_uri, parameters)
# deploy a template referenced by a URI, with parameters as a JSON string
def deploy_template_uri(access_token, subscription_id, resource_group, deployment_name, template_uri, parameters):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.Resources/deployments/', deployment_name,
                        '?api-version=', BASE_API])
    body = ''.join(['{   "properties": {     "templateLink": {       "uri": "', template_uri,
                    '",       "contentVersion": "1.0.0.0"     },',
                    '     "mode": "Incremental",',
                    '     "parameters": ', parameters,
                    '   } }'])
    return do_put(endpoint, body, access_token)


# deploy_template_uri_param_uri(access_token, subscription_id, resource_group, deployment_name, template_uri, parameters_uri)
# deploy a template with both template and parameters referenced by URIs
def deploy_template_uri_param_uri(access_token, subscription_id, resource_group, deployment_name, template_uri,
                                  parameters_uri):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', resource_group,
                        '/providers/Microsoft.Resources/deployments/', deployment_name,
                        '?api-version=', BASE_API])
    body = ''.join(['{   "properties": {     "templateLink": {       "uri": "', template_uri,
                    '",       "contentVersion": "1.0.0.0"     },     "mode": "Incremental",     "parametersLink": {       "uri": "',
                    parameters_uri, '",       "contentVersion": "1.0.0.0"           }   } }'])
    return do_put(endpoint, body, access_token)
