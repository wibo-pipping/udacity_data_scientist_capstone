import json
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from plotly.utils import PlotlyJSONEncoder

from common import get_today_date_str


def generate_line_graph_json(df: pd.DataFrame, ticker_symbol: str) -> json:
    """Takes a pandas DataFrame and generates the graphJSON object needed to plot a line chart"""
    
    fig = px.line(df, x=df.index, y='7d_rolling_avg', title=f'7 day rolling average for ticker: {ticker_symbol!r}')

    # Add vertical line for today
    fig.add_vline(x=get_today_date_str(), line_width=1, line_dash='dot', line_color='#e377c2')

    # TODO:
    ## Change line color for historic data vs forecasted data

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