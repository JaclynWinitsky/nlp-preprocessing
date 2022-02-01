#Import libraries
import argparse
import csv
import json
import sys

import boto3
import botocore
import botocore.client
from bs4 import BeautifulSoup
from smart_open import open
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import string

# setup cmd argument parser
parser = argparse.ArgumentParser(
    description= 'data extraction and preprocessing for NLP from a ndjson'
)
parser.add_argument('--source',help='source file to read data from',required=True)
parser.add_argument('--destination',help='destination file to write data to',required=True)
args = parser.parse_args()

# set up botocore client for ananoymous S3 access
config = botocore.client.Config(signature_version=botocore.UNSIGNED)
params = {'client': boto3.client('s3', config=config)}

# opening source nbjson file with exception handling 
try:
    with open(args.source, transport_params=params) as f:
        # parse ndjson lines and convert to list of dictionaries
        data = list(map(json.loads, f.readlines()))
except FileNotFoundError:
    sys.exit("ERROR: File doesn't exist: " + args.source)
except OSError:
    sys.exit("ERROR: Couldn't open s3 bucket: " + args.source)
except:
    sys.exit("ERROR: Couldn't open source: " + args.source)
    
# check if the note section is not empty, used in filter below
def has_content(x):
    return x["note"] != None and str(x["note"]).strip() != ""

# filter the data from the empty notes
data = list(filter(has_content, data))

# feature to remove the punctuation from notes 
def remove_punctuation(text):
    return "".join([char for char in text if char not in string.punctuation])

# remove stopwords to simplify the notes 
def remove_stopwords(text):
    #first tokenize text 
    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)
    return [word for word in text if word not in stopwords.words('english')]

# make new list of dictionaries with correct headers to export 
output =  []
for row in data:
    extracted = BeautifulSoup(str(row["note"]),"html.parser").get_text().strip()
    output.append({
        "note_id": row["id_note"],
        "client_id":row["patient_id"],
        "raw_note":row["note"],
        "clean_note": extracted,
        "note_length": len(extracted),
        "note_no_punct": remove_punctuation(extracted),
        "note_no_stopwords": remove_stopwords(extracted)
    })

# write output to csv file 
fieldnames = ['note_id', 'client_id', 'raw_note','clean_note','note_length','note_no_punct','note_no_stopwords']
with open(args.destination, 'w') as file:
    writer = csv.DictWriter(file, fieldnames)
    writer.writeheader()
    writer.writerows(output)

print("Succesfully extracted and processed data to " + args.destination)