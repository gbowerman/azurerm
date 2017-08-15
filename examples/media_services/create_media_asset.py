"""
Copyright (c) 2016, Marcelo Leal
Description: Simple Azure Media Services Python library
License: MIT (see LICENSE.txt file for details)
"""
import os
import json
import amspy
import time
#import pytz
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

#Some global vars...
name = "testasset"

### create an asset
print ("\n001 >>> Creating a Media Asset")
response = amspy.create_media_asset(access_token, name)
if (response.status_code == 201):
	resjson = response.json()
	asset_id = str(resjson['d']['Id']);
	print("POST Status.............................: " + str(response.status_code))
	print("Media Asset Name........................: " + name)
	print("Media Asset Id..........................: " + asset_id)
else:
	print("POST Status.............................: " + str(response.status_code) + " - Media Asset: '" + name + "' Creation ERROR." + str(response.content))

