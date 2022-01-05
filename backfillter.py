import pandas as pd
import numpy as np
import requests
import json
import concurrent.futures
from decouple import config

# Disable warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BackFillter:
    def __init__(self):
        self.EOD_API_KEY = config("EOD_API_KEY")
        self.FMP_API_KEY = config("FMP_API_KEY")

    def get_jsonparsed_data(self, url):
        """
        Sends a GET request to EOD's API and returns the resulting data in a dictionary
        """
        # sending get request and saving the response as response object
        response = requests.get(url=url)
        data = json.loads(response.text)
        return data

    def backfill_earnings(self):
        # Read in nasdaq data and extract symbols column
        nasdaq_list = pd.read_csv("nasdaq_list.csv")
        # Filtering data
        filtered_df = nasdaq_list[nasdaq_list["Market Cap"] > 1000000000]
        # Pull the column of stock symbols
        symbols = filtered_df.Symbol

        url_list = []
        for idx, val in enumerate(symbols):
            url = "https://financialmodelingprep.com/api/v3/historical/earning_calendar/{}?limit=80&apikey={}".format(val, FMP_API_KEY)
            url_list.append(url)
        
        # Call FMP API for each URL using Concurrent library
        # Run takes 211 seconds ... be patient
        with concurrent.futures.ThreadPoolExecutor() as executor:
            res = [executor.submit(self.get_jsonparsed_data, url) for url in url_list]
            concurrent.futures.wait(res)

        df = pd.DataFrame()
        ve_num = 0
        for x in range(len(symbols)):
            try:
                res_df = pd.DataFrame.from_records(res[x].result())
                df = pd.concat([df, res_df])
            # If value error occurs skip the stock
            except ValueError as e:
                ve_num += 1
                pass
        print("There were {} stocks skipped.".format(ve_num))

        # Filter earings for last 10 years of data
        filtered_earnings = df.loc[(pd.to_datetime(df['date']) > '2012-01-01')]
        # Drop revenue and revenueEstimated columns
        filtered_earnings = filtered_earnings.drop(['revenue', 'revenueEstimated'], axis = 1)
        # Drop any rows with null values
        filtered_earnings = filtered_earnings.dropna()
        return filtered_earnings

    def backfill_ohlc(self):
        # Read in earnings data and extract symbols column
        earnings_df = pd.read_csv("historical_earnings.csv")
        # Gather dates to iterate over
        dates = earnings_df["date"]

        # Build a list of url's that we will make API requests to:
        url_list = []
        for idx, val in enumerate(dates):
            ticker = earnings_df.symbol[idx]
            url = "https://financialmodelingprep.com/api/v3/historical-price-full/{}?from={}&to={}&apikey={}".format(ticker, val, val, self.FMP_API_KEY)
            url_list.append(url)

        # Shorter url_list for testing
        # urls = url_list[:4]

        # Call FMP API for each URL using Concurrent library
        # Take 45 minutes to run
        with concurrent.futures.ThreadPoolExecutor() as executor:
            res = [executor.submit(self.get_jsonparsed_data, url) for url in url_list]
            concurrent.futures.wait(res)

        na_row = {
            'symbol': [np.nan],
            'date': [np.nan],
            'open': [np.nan],
            'high': [np.nan],
            'low': [np.nan],
            'close': [np.nan],
            'adjClose': [np.nan],
            'volume': [np.nan],
            'unadjustedVolume': [np.nan],
            'change': [np.nan],
            'changePercent': [np.nan],
            'vwap': [np.nan],
            'label': [np.nan],
            'changeOverTime': [np.nan]
        }

        na_df = pd.DataFrame.from_dict(na_row)

        df = pd.DataFrame()
        ve_num = 0
        ke_num = 0
        for x in range(len(url_list)):
            try:
                res_df = pd.DataFrame.from_records(res[x].result()["historical"])
                stock = pd.DataFrame.from_records(res[x].result())["symbol"]
                res_df.insert(0, "symbol", stock)
                df = pd.concat([df, res_df])
            # If value error occurs skip the stock
            except ValueError as ve:
                ve_num += 1
                print(ve)
                pass
            # If KeyError occurs it is most likely due to timeout
            except KeyError as ke:
                ke_num += 1
                df = pd.concat([df, na_df])
                message = "KeyError at index: {}, url: {}, occurence number: {}".format(x, url, ke_num)
                # Log the error in a txt file with the index and url that failed
                with open("error_logs.txt", "a") as text_file:
                    text_file.write(message)
                    text_file.write('\n')
                print("KeyError at index: {}".format(x))
        return df

if __name__ == "__main__":
    backfiller = BackFillter()
    # Uncomment to backfill earnings data
    # earnings = backfiller.backfill_earnings()
    # earnings.to_csv("historical_earnings.csv", index=False)

    # Backfill OHLC pricing data
    ohlc_data_df = backfiller.backfill_ohlc()
    ohlc_data_df.to_csv("ohlc_output.csv", index=False)
