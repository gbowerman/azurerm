# azurerm unit tests

The azurerm unit tests have the following principles:

- Each azurerm function call is tested by at least one unit test.
- Each new azurerm function checkin should have a unit test associated with it.
- All affected unit tests pass before a code change is checked in. Affected means tests which directly or indirectly cause the modified code to run.
- Certain checkins with large potential effects, like modifying an API version require all unit tests to pass. 

Note 9/12/16: Formalized unit tests are a new addition and it will be a while before they have effective coverage.

## Installation
1. Install dependent libraries: unittest, pyhaikunator, json, azurerm
2. Copy azurermconfig.json.tmpl to azurermconfig.json and fill in settings that work in your test environment, and desired Azure location etc.

## Using azurerm unittests
```
cd azurerm/test
python -m unittest <testfile.py>
```

e.g. 
```
python -m unittest resource_groups_test.py
```