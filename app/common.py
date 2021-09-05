import datetime as dt
import json

DATE_FORMAT = '%Y-%m-%d'

def get_supported_tickers():
    """Read a json file with properties per ticker. Return list of tickers"""
    with open('params/prophet_params.json') as f:
        d_ = json.load(f)

    return list(d_.keys())


def get_today_date_str():
    """Return todays date as a string"""
    return dt.date.today().strftime(DATE_FORMAT)


def get_today_epoch():
    """Return the epoch timestamp in miliseconds"""
    # Use get_today_date to get specific timepoint in the day
    return dt.datetime.strptime(get_today_date_str(), DATE_FORMAT).timestamp()*1000