# Data Extraction and pre-processing for NLP

## Description

The following script loads some raw home-health visit notes from a local or remote location, cleans the data, and extracts some valuable hand-crafted features from the notes. 

## Motivation 

Agencies that use AlayaCare have a wealth of unstructured visit notes stored on their Alayacare Cloud instances. These notes are left by caregivers every time they visit a patient. Alayalabs, wants to put this unstructured data to work for their customers by using it to predict the probability of adverse events like the patient falling or landing in the emergency room. This model will obtain these notes from a database, parse the response, and extract clean features that can then be used to train models and inference pipelines.

## Dependencies 

 You must have [python](https://www.python.org/downloads/) installed first. This project relies on three libraries:
 
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for extracting text from HTML and [smart-open](https://pypi.org/project/smart-open/) with [Boto3](https://aws.amazon.com/sdk-for-python/?nc=hl&pg=gs&p=s3) to read S3 libraries. 

You can install both dependencies by using:

```
pip install bs4 boto3 smart-open
```

## Usage

To run, use: 

```
python task.py --source <path> --destination <path>
```

### Arguments:

|name|description|required|
|---|---|---|
|source|source file to read data from, either a local file or an s3 bucket url. Data must be in [ndjson](http://ndjson.org/) |true|
|destination|destination file, either a local file or an s3 bucket url|true|

You can get help by using: 

```
python clean_data.py -h
```
