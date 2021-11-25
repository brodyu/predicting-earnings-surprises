#!/usr/bin/env python

from decouple import config
import requests


def get_jsonparsed_data(url, YEAR):
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
    text_data = response.text
    # Write response to text file
    with open("data/bulk_suprises_{}.txt".format(YEAR), "w") as text_file:
        text_file.write(text_data)


if __name__ == "__main__":
    # Pull API key from .env file
    FMP_API_KEY = config("FMP_API_KEY")
    # Input: year to pull for bulk endpoint
    YEAR = 2019

    url = "https://financialmodelingprep.com/api/v4/earnings-surprises-bulk?year={}&apikey={}".format(
        YEAR, FMP_API_KEY)

    try:
        data = get_jsonparsed_data(url, YEAR)
    except Exception as e:
        print(e)
