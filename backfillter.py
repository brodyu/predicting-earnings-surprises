import pandas as pd
import numpy as np
import time
import requests
import json
import concurrent.futures
from decouple import config

class BackFillter:
    def __init__(self):
        self.EOD_API_KEY = config("EOD_API_KEY")

    def get_jsonparsed_data(self, url):
        """
        Sends a GET request to EOD's API and returns the resulting data in a dictionary
        """
        # sending get request and saving the response as response object
        response = requests.get(url=url)
        data = json.loads(response.text)
        return data

    def backfill_ohlc_data(self):

        earnings_df = pd.read_csv("data/historical_earnings.csv")
        dates = earnings_df["date"]
        print(earnings_df.symbol[0])

        # Build a list of url's that we will make API requests to:
        url_list = []
        for idx, val in enumerate(dates):
            ticker = earnings_df.symbol[idx]
            url = "https://eodhistoricaldata.com/api/eod/{}.US?fmt=json&from={}&to={}&period=d&api_token={}".format(ticker, val, val, self.EOD_API_KEY)
            url_list.append(url)

        print("Working...")
        
        url = url_list[2]
        data = self.get_jsonparsed_data(url)
        print(data)

if __name__ == "__main__":
    backfiller = BackFillter()
    ohlc_data = backfiller.backfill_ohlc_data()