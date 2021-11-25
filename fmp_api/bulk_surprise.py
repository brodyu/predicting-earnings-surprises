#!/usr/bin/env python

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import certifi
import json
from decouple import config
import requests


def get_jsonparsed_data(url, YEAR):
    # sending get request and saving the response as response object
    response = requests.get(url = url)
    text_data = response.text
    # Write response to text file
    with open("bulk_suprises_{}.txt".format(YEAR), "w") as text_file:
        text_file.write(text_data)

FMP_API_KEY = config("FMP_API_KEY")
YEAR = 2020

url = "https://financialmodelingprep.com/api/v4/earnings-surprises-bulk?year={}&apikey={}".format(YEAR, FMP_API_KEY)
print(url)
try:
    data = get_jsonparsed_data(url, YEAR)
except Exception as e:
    print(e)