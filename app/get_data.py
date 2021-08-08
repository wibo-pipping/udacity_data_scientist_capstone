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

def create_bar_chart():
    # Create simple barchart to see if this works in webapp world
    df = pd.DataFrame({
      'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 'Bananas'],
      'Amount': [4, 1, 2, 2, 4, 5],
      'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
      })
    
    fig = px.bar(df, x='Fruit', y='Amount', color='City', barmode='group')

    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)

    return graphJSON

def create_line_chart(df: pd.DataFrame, ticker_symbol: str) -> json:
    df['7d_rolling_avg'] = df.rolling(window=7).adj_close.mean()

    fig = px.line(df, x=df.index, y='7d_rolling_avg', title=f'7 day rolling average for ticker: {ticker_symbol!r}')

    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)

    return graphJSON


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