"""
Copyright (c) 2016, Marcelo Leal
Description: Simple Azure Media Services Python library
License: MIT (see LICENSE.txt file for details)
"""
import os
import json
import amspy
import time
import sys
#import pytz
import urllib
import logging
import datetime
from azure import *
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings


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

#The Output AssetID to download all files from
OUTPUTASSETID = "nb:cid:UUID:e472aee0-2fc2-40e5-9271-4595f9acc3f4"

# Load Azure app defaults
try:
	with open('../config.json') as configFile:
		configData = json.load(configFile)
except FileNotFoundError:
	print("ERROR: Expecting config.json in examples folder")
	sys.exit()


account_name = configData['accountName']
account_key = configData['accountKey']
sto_account_name = configData['sto_accountName']
sto_accountKey = configData['sto_accountKey']
log_name = configData['logName']
log_level = configData['logLevel']
purge_log = configData['purgeLog']

# Get a fresh API access token...
response = amspy.get_access_token(account_name, account_key)
resjson = response.json()
access_token = resjson["access_token"]

# Get Asset by using the list_media_asset method and the Asset ID
response = amspy.list_media_asset(access_token,OUTPUTASSETID)
if (response.status_code == 200):
    resjson = response.json()
    # Get the container name from the Uri
    outputAssetContainer = resjson['d']['Uri'].split('/')[3]
    print(outputAssetContainer)


### Use the Azure Blob Blob Service library from the Azure Storage SDK.
block_blob_service = BlockBlobService(account_name=sto_account_name,account_key=sto_accountKey)
generator = block_blob_service.list_blobs(outputAssetContainer)
for blob in generator:
    print(blob.name)
    if(blob.name.endswith(".vtt")):
        blobText = block_blob_service.get_blob_to_text(outputAssetContainer, blob.name)
        print("\n\n##### WEB VTT ######")
        print(blobText.content)
        block_blob_service.get_blob_to_path(outputAssetContainer, blob.name, "output/" + blob.name)