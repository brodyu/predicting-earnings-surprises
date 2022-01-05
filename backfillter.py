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
        start_time = time.time()
        earnings_df = pd.read_csv("data/historical_earnings.csv")
        dates = earnings_df["date"]

        # Build a list of url's that we will make API requests to:
        url_list = []
        for idx, val in enumerate(dates):
            ticker = earnings_df.symbol[idx]
            url = "https://eodhistoricaldata.com/api/eod/{}.US?fmt=json&from={}&to={}&period=d&api_token={}".format(ticker, val, val, self.EOD_API_KEY)
            url_list.append(url)

        print("Working...")

        df = pd.DataFrame()
        ve_num = 0
        ce_num = 0

        # URL subset for testing
        # urls = url_list[:3]

        for idx, val in enumerate(url_list):
            try: 
                print("Current Iteration: {}".format(idx))
                ticker = earnings_df.symbol[idx]
                data = self.get_jsonparsed_data(val)
                # Convert to dataframe
                res_df = pd.DataFrame.from_records(data)
                res_df.insert(0, "Symbol", ticker)
                df = pd.concat([df, res_df], ignore_index=True)
                print("--- %s seconds ---" % (time.time() - start_time))
            # If value error occurs skip the stock
            except ValueError as ve:
                ve_num += 1
                print("ValueError encountered...")
                print("Current ValueError count: {}".format(ve_num))
                pass
            except ConnectionError as ce:
                ce_num += 1
                print("ConnectionError encountered...")
                print("Current ConnectionError count: {}".format(ve_num))
                pass
        return df


if __name__ == "__main__":
    backfiller = BackFillter()
    ohlc_data_df = backfiller.backfill_ohlc_data()
    ohlc_data_df.to_csv("ohlc_test.csv", index=False)