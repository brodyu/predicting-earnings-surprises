#!/usr/bin/env python

from decouple import config
import requests
import json

def get_jsonparsed_data(url):
    """
    Sends a GET request to FMP's Bulk Earning Surprise API and writes the results to a txt file.

    Parameters
    ----------
    url : str
    YEAR : int

    Returns
    -------
    None
    """
    # sending get request and saving the response as response object
    response = requests.get(url=url)
    text_data = json.loads(response.text)
    return text_data


if __name__ == "__main__":
    # Pull API key from .env file
    FMP_API_KEY = config("FMP_API_KEY")
    # Input: year to pull for bulk endpoint
    YEAR = 2019
    stock = "MSFT"
    start_date = "2019-01-01"
    end_date = "2020-01-01"

    url = "https://financialmodelingprep.com/api/v3/historical-price-full/{}?from={}&to={}&apikey={}".format(stock, start_date, end_date,FMP_API_KEY)

    try:
        data = get_jsonparsed_data(url)
        print(data)
    except Exception as e:
        print(e)
