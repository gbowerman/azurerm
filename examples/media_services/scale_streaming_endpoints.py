"""
Copyright (c) 2016, Marcelo Leal
Description: Simple Azure Media Services Python library
License: MIT (see LICENSE.txt file for details)
"""
import os
import json
import amspy
import time
import logging
import datetime

###########################################################################################
##### DISCLAIMER ##### ##### DISCLAIMER ##### ##### DISCLAIMER ##### ##### DISCLAIMER #####
###########################################################################################

# ALL CODE IN THIS DIRECTOY (INCLUDING THIS FILE) ARE EXAMPLE CODES THAT  WILL  ACT ON YOUR
# AMS ACCOUNT.  IT ASSUMES THAT THE AMS ACCOUNT IS CLEAN (e.g.: BRAND NEW), WITH NO DATA OR
# PRODUCTION CODE ON IT.  DO NOT, AGAIN: DO NOT RUN ANY EXAMPLE CODE AGAINST PRODUCTION AMS
# ACCOUNT!  IF YOU RUN ANY EXAMPLE CODE AGAINST YOUR PRODUCTION  AMS ACCOUNT,  YOU CAN LOSE
# DATA, AND/OR PUT YOUR AMS SERVICES IN A DEGRADED OR UNAVAILABLE STATE. BE WARNED!

###########################################################################################
##### DISCLAIMER ##### ##### DISCLAIMER ##### ##### DISCLAIMER ##### ##### DISCLAIMER #####
###########################################################################################

# Load Azure app defaults
try:
	with open('config.json') as configFile:
		configData = json.load(configFile)
except FileNotFoundError:
	print("ERROR: Expecting config.json in current folder")
	sys.exit()

account_name = configData['accountName']
account_key = configData['accountKey']

# Get the access token...
response = amspy.get_access_token(account_name, account_key)
resjson = response.json()
access_token = resjson["access_token"]

#Initialization...
print ("\n-----------------------= AMS Py =----------------------");
print ("Simple Python Library for Azure Media Services REST API");
print ("-------------------------------------------------------\n");

#some global vars...
SCALE_UNIT = "1"

print ("\n001 >>> Scaling a Streaming Endpoint")
# list and get the id of the default streaming endpoint
response = amspy.list_streaming_endpoint(access_token)
if (response.status_code == 200):
        resjson = response.json()
        for ea in resjson['d']['results']:
                print("POST Status.............................: " + str(response.status_code))
                print("Streaming Endpoint Id...................: " + ea['Id'])
                print("Streaming Endpoint Name.................: " + ea['Name'])
                print("Streaming Endpoint Description..........: " + ea['Description'])
                if (ea['Name'] == 'default'):
                        streaming_endpoint_id = ea['Id'];
else:
        print("POST Status.............................: " + str(response.status_code) + " - Streaming Endpoint Creation ERROR." + str(response.content))
### scale the default streaming endpoint
response = amspy.scale_streaming_endpoint(access_token, streaming_endpoint_id, SCALE_UNIT)
if (response.status_code == 202):
        print("POST Status.............................: " + str(response.status_code))
        print("Streaming Endpoint SU Configured to.....: " + SCALE_UNIT)
else:
        print("GET Status.............................: " + str(response.status_code) + " - Streaming Endpoint Scaling ERROR." + str(response.content))
