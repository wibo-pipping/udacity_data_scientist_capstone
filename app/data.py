from pandas.core.frame import DataFrame
import yfinance as yf
import pandas as pd

from common import get_today_date_str


def get_clean_ticker_data(ticker_symbol: str, start_date: str='2019-01-01', end_date:str=get_today_date_str()) -> pd.DataFrame:
    """Retrieve the ticker data between start and end dates and return a DataFrame with cleaned and enriched data.

    Keyword arguments:
    ticker_symbol -- Valid ticker symbol to retrieve data for
    start_date    -- Start date to retieve data for, string (default '2021-01-01')
    end_date      -- End date to retrieve data for, string (default date of today)
    """

    ticker_data = get_ticker_data(ticker_symbol, start_date, end_date)
    clean_ticker_data = preprocess_ticker_data(ticker_data)
    enriched_ticker_data = enrich_ticker_data(clean_ticker_data)

    return enriched_ticker_data


def get_ticker_data(ticker_symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Retrieve the data through the yahoo finance API between start and end dates and return a pandas DataFrame with
    the adjusted close values per day. Return the dataframe with the downloaded data

    Keyword arguments:
    ticker_symbol -- Valid ticker symbol to retrieve data for
    start_date    -- Start date to retieve data for, string (default '2021-01-01')
    end_date      -- End date to retrieve data for, string (default date of today)
    """

    df =  yf.download(ticker_symbol, start=start_date, end=end_date)

    return df


def preprocess_ticker_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the ticker data by filling in the empty/missing dates with last known values.
    Clean the column names to be lower case and replace whitespaces with underscores
    Requires a date range index and assumes data is daily.
    """

    df = df.resample('D').ffill()
    df.columns = df.columns.str.lower().str.replace(' ','_')

    return df


def enrich_ticker_data(df: pd.DataFrame) -> pd.DataFrame:
    """Enrich the ticker data with a 7d rolling window average value"""
    
    df['7d_rolling_avg'] = df.rolling(window=7).adj_close.mean()

    return df
