#!/usr/bin/env python

import time
import logging
import pandas as pd
from decouple import config
import requests
import json
import concurrent.futures
import aiotasks


# Disable warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_jsonparsed_data(url):
    """
    Sends a GET request to FMP's Earning Surprise API and returns the resulting data in a dictionary
    """
    # sending get request and saving the response as response object
    response = requests.get(url=url)
    data = json.loads(response.text)
    return data


if __name__ == "__main__":
    start_time = time.time()
    # Read in nasdaq data and extract symbols column
    nasdaq_list = pd.read_csv("data/nasdaq_list.csv")
    # Pull API key from .env file
    FMP_API_KEY = config("FMP_API_KEY")

    print(nasdaq_list.info())

    # Filter missing out rows with missing data
    # Filter reduces dataset from 8202 entries to 3156 entries
    nasdaq_list_filtered = nasdaq_list.dropna()
    print("---"*7)
    print(nasdaq_list_filtered.info())
    print("---"*7)
    symbols = nasdaq_list_filtered.Symbol

    url_list = []
    for idx, val in enumerate(symbols):
        url = "https://financialmodelingprep.com/api/v3/earnings-surprises/{}?apikey={}".format(val, FMP_API_KEY)
        url_list.append(url)
    
    # Call FMP API for each URL using Concurrent library
    # Run takes 211 seconds ... be patient
    with concurrent.futures.ThreadPoolExecutor() as executor:
        res = [executor.submit(get_jsonparsed_data, url) for url in url_list]
        concurrent.futures.wait(res)

    df = pd.DataFrame()
    for x in range(len(symbols)):
        res_df = pd.DataFrame(res[x].result())
        pd.concat([df, res_df])

    df.to_csv("data/nasdaq_earnings.csv")
    logging.critical("Multithread execution time in seconds: %f" % (time.time()-start_time))