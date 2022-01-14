import pandas as pd
import json
import requests
import pymysql
from sqlalchemy import create_engine, MetaData, Table, insert
from sqlalchemy.orm import sessionmaker
from decouple import config
from datetime import date

# Set parameters for AWS database
aws_hostname = config("AWS_HOST")
aws_database = config("AWS_DB")
aws_username = config("AWS_USER")
aws_password = config("AWS_PASS")
aws_port = config("AWS_PORT")

# Pull API keys from .env file
FMP_API_KEY = config("FMP_API_KEY")
EOD_API_KEY = config("EOD_API_KEY")

def get_jsonparsed_data(url):
    """
    Sends a GET request to API and returns the resulting data in a dictionary
    """
    # sending get request and saving the response as response object
    response = requests.get(url=url)
    data = json.loads(response.text)
    return data

def create_unique_id(df):
    """
    Creates unique_id used in database as primary key
    """
    # Create unique identifier and append to list
    id_list = []
    for idx, row in df.iterrows():
        symbol = row["symbol"]
        date = row["date"]
        unique_id = date + '-' + symbol
        id_list.append(unique_id)
    # Insert IDs into dataframe as new column
    df.insert(0, "id", id_list)
    return df

def clean_earnings_data(df):
    """
    Clean earnings data by:
    - Filtering out ADRs and other exchanges
    - Removing stocks that have any null values in epsEstimated, or time
    - Dropping revenue and revenueEstimated columns
    - Creating a unique ID
    """
    # If ticker is greater than a length of 5, drop it
    df["length"] = df.symbol.str.len()
    df = df[df.length < 5]
    # Filter missing columns out
    df = df.dropna(subset=['date', 'symbol','epsEstimated', 'time'])
    # Drop unwanted columns
    df = df.drop(['revenue', 'revenueEstimated', 'length'], axis=1)
    df = create_unique_id(df)
    df = df.rename({'date':'earnings_date','epsEstimated':'eps_estimated', 'time':'earnings_time'}, axis=1)
    return df

def clean_pricing_data(df):
    """
    Clean pricing data by:
    - Removing label column
    - Creating a unique ID
    """
    df = df.drop(['label'], axis=1)
    df = create_unique_id(df)
    df = df.rename({'date':'earnings_date','open':'open_price', 'high':'high_price', 'low':'low_price',
                    'close':'close_price', 'adjClose': 'adj_close', 'volume':'daily_volume',
                    'unadjustedVolume':'unadjusted_volume', 'change':'change_dollars', 
                    'changePercent':'change_percent', 'changeOverTime':'change_over_time'}, axis=1)
    return df


if __name__ == "__main__":
    # Setup SQL Alchemy for AWS database
    sqlalch_conn = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(aws_username, aws_password, aws_hostname, aws_database)
    engine = create_engine(sqlalch_conn, echo=False)

    # Connect to FMP API and pull earnings data
    today = str(date.today())
    earnings_res = get_jsonparsed_data("https://financialmodelingprep.com/api/v3/earning_calendar?from={}&to={}&apikey={}".format(today, today, FMP_API_KEY))
    earnings_df = pd.DataFrame(earnings_res)

    # Filter earnings data
    earnings_filtered = clean_earnings_data(earnings_df)
    print(earnings_filtered)

    try:
        earnings_filtered.to_sql("earnings_test", con=engine, index=False, if_exists='append')
    except Exception as e:
        print(e)

    # Pull list of symbols
    symbols = earnings_filtered.symbol
    # For each symbol pull today's pricing
    pricing_df = pd.DataFrame()
    for symbol in symbols:
        url = "https://financialmodelingprep.com/api/v3/historical-price-full/{}?from={}&to={}&apikey={}".format(symbol, today, today, FMP_API_KEY)
        res = get_jsonparsed_data(url)
        res_df = pd.DataFrame.from_records(res["historical"])
        # Insert symbol
        res_df.insert(1, "symbol", symbol)
        # Concat with main dataframe
        pricing_df = pd.concat([pricing_df, res_df])
    # Filter pricing data
    pricing_filtered = clean_pricing_data(pricing_df)
    print(pricing_filtered)