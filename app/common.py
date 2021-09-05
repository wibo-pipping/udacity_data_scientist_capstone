import datetime as dt

DATE_FORMAT = '%Y-%m-%d'


def get_today_date_str():
    """Return todays date as a string"""
    return dt.date.today().strftime(DATE_FORMAT)


def get_today_date_str():
    """Return the epoch timestamp in miliseconds"""
    return dt.datetime.strptime(get_today_date_str(), DATE_FORMAT).timestamp()*1000