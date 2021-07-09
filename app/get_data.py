import yfinance as yf
import pandas as pd
import datetime as dt
from typing import Optional

DEFAULT_END_DATE = dt.date.today().strftime('%Y-%m-%d')


def get_ticker_data(ticker_symbol: str, start_date: str='2021-01-01', end_date: str=DEFAULT_END_DATE) -> pd.DataFrame:
    """Retrieve the data through the yahoo finance API between start and end dates and return a pandas DataFrame with
    the adjusted close values per day.

    Keyword arguments:
    ticker_symbol -- Valid ticker symbol to retrieve data for
    start_date    -- Start date to retieve data for, string (default '2021-01-01')
    end_date      -- End date to retrieve data for, string (default date of today)
    """

    df =  yf.download(ticker_symbol, start=start_date, end=end_date)

    df.columns = df.columns.str.lower().str.replace(' ','_')

    return df[['adj_close']].to_html()