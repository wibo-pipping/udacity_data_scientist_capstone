import json
import yfinance as yf
import pandas as pd
import datetime as dt

import plotly.graph_objects as go
import plotly.express as px

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


def generate_line_graph_json(df: pd.DataFrame, ticker_symbol: str) -> json:
    """Takes a pandas DataFrame, calculates a moving average and returns the graphJSON object to plot a line chart"""
    # TODO: move out the calculation/Dataframe logic out to its own function
    df['7d_rolling_avg'] = df.rolling(window=7).adj_close.mean()

    fig = px.line(df, x=df.index, y='7d_rolling_avg', title=f'7 day rolling average for ticker: {ticker_symbol!r}')

    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)

    return graphJSON


# TODO: evaluate if I want to use this.
def create_candle_json(df, ticker_symbol):
    fig = go.Figure(data=[
        go.Candlestick(
            x=df.index,
            open=df.open,
            high=df.high,
            low=df.low,
            close=df.adj_close,
            increasing=dict(line=dict(color= '#17BECF')),
            decreasing=dict(line=dict(color= '#7F7F7F')),
            name=ticker_symbol
            )
        ])

    fig.update_layout(xaxis_rangeslider_visible = False)

    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)

    return graphJSON