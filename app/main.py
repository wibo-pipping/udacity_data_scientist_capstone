from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

from .get_data import get_ticker_data

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

@app.get('/')
def home(request: Request):
    """
    Displays the homepage.
    """
    result = "Type a ticker symbol"
    return templates.TemplateResponse("home.html", context={'request': request, 'result': result})


@app.post("/")
def form_post(request: Request, ticker_symbol: str = Form(...)):
    result = get_ticker_data(ticker_symbol)

    context = { 'request': request,
                'result': result,
                'ticker_symbol': ticker_symbol
                }

    return templates.TemplateResponse('home.html', context=context)