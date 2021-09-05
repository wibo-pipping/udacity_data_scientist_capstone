import pandas as pd
import json

from pandas.core.indexes.numeric import IntegerIndex
from fbprophet import Prophet


def forecast_data(df: pd.DataFrame, ticker_symbol: str, forecast_column: str='adj_close') -> pd.DataFrame:
    """Get the dataframe with ticker symbol and run the forecast. Retrieves model parameters for the ticker symbol to optimize performance.
    Use `forecast_column` to select the column to forecast for. Merges the forecasted data with the 
    """

    index_name = df.index.name
    df = df.reset_index(drop=False)
    df = df.rename(columns={index_name:'ds', forecast_column:'y'})

    model_params = get_prophet_params(ticker_symbol)

    forecast = forecast_with_prophet(df[['ds','y']], prophet_params=model_params)

    result = df.merge(forecast, on='ds', how='outer')
    result = result.set_index('ds', drop=False)

    return result


def get_prophet_params(ticker_symbol: str) -> dict:
    """Read the parameters for prophet from disk and select the params for the current ticker"""
    
    with open('params/prophet_params.json','r') as f:
        all_params = json.load(f)
    
    prophet_params = all_params.get(ticker_symbol, {})

    return prophet_params


def forecast_with_prophet(df: pd.DataFrame, days: int=180, prophet_params:dict = {}) -> pd.DataFrame:
    """Use prophet to create a model, fit the data and forecast"""

    model = Prophet(**prophet_params)
    model.fit(df)
    future_df = model.make_future_dataframe(periods=days)
    forecast = model.predict(future_df)

    return forecast
