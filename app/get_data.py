import json
import yfinance as yf
import pandas as pd
import datetime as dt

import plotly.graph_objects as go

from plotly.utils import PlotlyJSONEncoder

from typing import Optional

DEFAULT_END_DATE = dt.date.today().strftime('%Y-%m-%d')


def get_ticker_data(ticker_symbol: str, start_date: str='2021-01-01', end_date: str=DEFAULT_END_DATE) -> pd.DataFrame:
    """Retrieve the data through the yahoo finance API between start and end dates and return a pandas DataFrame with
    the adjusted close values per day. Return the dataframe with the downloaded data

    Keyword arguments:
    ticker_symbol -- Valid ticker symbol to retrieve data for
    start_date    -- Start date to retieve data for, string (default '2021-01-01')
    end_date      -- End date to retrieve data for, string (default date of today)
    """

    df =  yf.download(ticker_symbol, start=start_date, end=end_date)

    df.columns = df.columns.str.lower().str.replace(' ','_')

    return df


def create_candle_json(df, ticker_symbol):
    fig = go.Figure(data=[
        go.Candlestick(
            x=df.index,
            open=df.open,
            high=df.high,
            low=df.low,
            close=df.adj_close,
            name=ticker_symbol)
            ]
        )

    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)

    return graphJSON