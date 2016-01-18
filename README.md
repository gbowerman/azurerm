# azurerm
Easy to use Python library for Azure Resource Manager

The azurerm philosophy is ease of use over completeness of API. Rather than support every possible attribute the goal is to provide a set of simple functions for the most common tasks.

## Installation
1. Clone the repo locally.
2. cd to the root directoy.
3. python setup.py install

## Using azurerm
To use this library (and in general to access Azure Resource Manager from a program) you need to register your application with Azure and create a "Service Principal" (an application equivalent of a user). Once you've done this you'll have 3 pieces of information: A tenant ID, an application ID, and an application secret. You will use these to create an authentication token.

For more information on how to get this information go here: <a href ="https://azure.microsoft.com/en-us/documentation/articles/resource-group-authenticate-service-principal/">Authenticating a service principal with Azure Resource Manager</a>. See also: <a href="https://msftstack.wordpress.com/2016/01/05/azure-resource-manager-authentication-with-python/">Azure Resource Manager REST calls from Python</a>.

### example to list Azure subscriptions
```
import azurerm

tenant_id = 'your-tenant-id'
application_id = 'your-aplication-id'
application_secret = 'your-aplication-secret'

# create an authentication token
access_token = azurerm.get_access_token(
    tenant_id,
    application_id,
    application_secret
)

# list subscriptions
subscriptions = azurerm.list_subscriptions(access_token)
for sub in subscriptions["value"]:
    print(sub["displayName"] + ': ' + sub["subscriptionId"])

# select the first subscription
subscription_id = subscriptions["value"][0]["subscriptionId"]

# create a resource group
print('Enter Resource group name to create.')
rgname = input()
location = 'southeastasia'
rgreturn = azurerm.create_resource_group(access_token, subscription_id, rgname, location)
print(rgreturn)

# list resource groups
resource_groups = azurerm.list_resource_groups(access_token, subscription_id)
for rg in resource_groups["value"]:
    print(rg["name"] + ', ' + rg["location"] + ', ' + rg["properties"]["provisioningState"])
```    
