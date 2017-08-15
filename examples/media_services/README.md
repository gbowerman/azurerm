## Pre-Req to run the samples
You will need to install the python sdk for Azure and Blob Storage (we use this sdk for the upload
part of our scripts), and install the amspy python library (this is the library that implements
the AMS REST API's).

```
pip(3) install pycrypto
pip(3) install azure
pip(3) install azure-storage
pip(3) install amspy
```

## Config File
You need to add your credentials and provide informaton about your AMS environment using the config
file (config.json). Here is a description of each option:
```
{
   "accountName": "<here-you-add-your-media-services-account-name>",
   "accountKey": "<here-you-add-your-media-services-account-secret-key>",
   "sto_accountName": "<your-storage-account-name>",
   "logName": "<here-you-choose-the-name-of-your-log-file>",
   "logLevel": "DEBUG",
   "purgeLog": "Yes",
}
```

## Examples
In this directory you have many small scripts that show how to use specific Azure Media Services API's.
You will also find two complete samples showing how to upload encode (or validate) assets, as well as
protect them and configure the streaming. You can see a description of these two scripts bellow...

## HLS+AES WORKFLOW (From MP4)

### Upload, validate, protect (dinamically with AES Envelope encryption), and stream your MP4 Videos.
This example does the complete AES workflow from uploading an already encode MP4 file,
validate it with the Azure Media Packager; protecting the asset with AES envelope encryption (content key
configuration, authorization policies, and etc), as well as configuring the HLS delivery policy.  
```
export PYTHONDONTWRITEBYTECODE=1; python3 aes_workflow_from_mp4.py
```

## HLS+AES WORKFLOW (From RAW)

### Upload, encode, protect (dinamically with AES Envelope encryption), and stream your Raw Video.
This example does the complete AES workflow from uploading an mezzanine video file,
encode it with the Azure Encoder; protecting the asset with AES envelope encryption (content key
configuration, authorization policies, and etc), as well as configuring the HLS delivery policy.  
```
export PYTHONDONTWRITEBYTECODE=1; python3 aes_workflow_from_raw.py
```
### Azure Media Analytics Usage Sample Scripts
A set of scripts that show how to use Azure Media Analytics is available in the amspy/examples/Analytics folder.
In this folder you will find examples of the following analytics tools:

- Face Detection
- Face Redaction
- Hyperlapse
- Indexer v1
- Indexer v2 (Preview)
- Motion Detection
- OCR
- Video Thumbnail

Each of the samples includes a single Python script and configuration file for the processor.
Simply execute the python script to process a source file.
To modify the source file used, edit the global variable and change the
VIDEO_PATH to point to your source file.

The script will execute and download the output results of the Media Analytics job into the "output" folder in the example.
You can modify the settings files for each processor to adjust the output results.

For additional documentation about Azure Media Analytics, plese refer to the page http://aka.ms/mediaanalytics

Please contact us on Twitter -  @MSFTAzureMedia - if you have any questions.
