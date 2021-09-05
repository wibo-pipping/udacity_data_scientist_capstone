from flask import Flask, render_template, request, jsonify
from data import get_clean_ticker_data
from graph import generate_line_graph_json
from forecast import forecast_data
from common import get_supported_tickers

app = Flask(__name__)

# Define the supported tickers
TICKERS = get_supported_tickers()


@app.route('/', methods=["GET"])
def home():
    """
    Displays the homepage.
    """

    return render_template('home.html', ticker_options=TICKERS)

@app.route('/', methods=['POST'])
def process_request():

    ticker_symbol = request.form.get('ticker_symbol',None)

    # Download the data
    df = get_clean_ticker_data(ticker_symbol)
    ticker_table = df.tail(10).loc[:,['adj_close']].T.to_html() ## TODO: turn this into a proper table

    # Forecast the data
    forecast = forecast_data(df, ticker_symbol)

    # Get graph object
    line_graphJSON = generate_line_graph_json(forecast, ticker_symbol)

    return render_template('home.html',
                           ticker_options=TICKERS, 
                           ticker_symbol=ticker_symbol,
                           ticker_table=ticker_table,
                           line_graphJSON = line_graphJSON
    )


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()