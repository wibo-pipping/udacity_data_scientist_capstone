import datetime as dt

DATE_FORMAT = '%Y-%m-%d'


def get_today_date_str():
    """Return todays date as a string"""
    return dt.date.today().strftime(DATE_FORMAT)


def get_today_epoch():
    """Return the epoch timestamp in miliseconds"""
    # Use get_today_date to get specific timepoint in the day
    return dt.datetime.strptime(get_today_date_str(), DATE_FORMAT).timestamp()*1000