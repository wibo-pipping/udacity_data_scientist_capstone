"""Small wrapper around quandle api to hide the API key from github in the jupyter notebook
"""

import os
import quandl

from dotenv import load_dotenv

import pandas as pd

load_dotenv()
quandl.ApiConfig.api_key = os.environ['QUANDLE_API_KEY']

def quandl_get(key):
    df = quandl.get(key)
    return df