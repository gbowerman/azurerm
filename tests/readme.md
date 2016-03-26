# azurerm test suite
Test scripts for **azurerm**.

These scripts are written to test azurerm functions, and can be used as an example library to build your Azure Python application. This is not an automated test suite. Some scripts can run as-is, some require input, and others require customization for your resources. 

To run these tests:

- Copy/clone the test library locally.
- Rename the azurermconfig.json.tmpl file to azurermconfig.json
- Edit azurermconfig.json, setting valid values for your test subcription id, tenant id, application id, application secret, resource group, VM Scale Set Name. not all of these values will be needed depending on which tests you run. For example VM tests won't need a VM Scale Set name.

