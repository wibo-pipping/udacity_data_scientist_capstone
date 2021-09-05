import json
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from plotly.utils import PlotlyJSONEncoder

from common import get_today_epoch


def generate_line_graph_json(df: pd.DataFrame, ticker_symbol: str, n_days_forecasted: int=180) -> json:
    """Takes a pandas DataFrame and generates the graphJSON object needed to plot a line chart"""

    fig = px.line(df,
                x=df.index,
                y='7d_rolling_avg',
                title=f'Stock price for {ticker_symbol}, forecasted to {n_days_forecasted} days into the future',
                labels={'index':'Date','7d_rolling_avg': 'Stock adjusted close ($)'},
                color_discrete_sequence=['#7d0c5b']
                )

    # Update the trace to display legend and format the hoverover field
    fig.update_traces(hovertemplate = '<b>Historic data</b><br>Date: %{x}<br>Stock adjusted close: $%{y}',
                  name='Historic data',
                  showlegend=True
                 )



    # Add vertical line for today
    fig.add_vline(x=get_today_epoch(),
                line={
                    'width':1.5,
                    'dash':'dot',
                    'color':'#e377c2'
                    },
                annotation_text='Today'
                )

    # Add scatter trace for forecasted data
    fig.add_trace(
    go.Scatter(
        x=df.iloc[-n_days_forecasted:].ds,
        y=df.iloc[-n_days_forecasted:].yhat,
        mode='markers',
        marker={
            'color': '#ebb2da',
            'symbol': 'hexagon2',
            'size': 10
        },
        opacity=1,
        name='Forecasted value',
        hovertemplate = '<b>Forecasted</b><br>Date: %{x}<br>Stock adjusted close: $%{y}'
        )
    )

    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)

    return graphJSON
    