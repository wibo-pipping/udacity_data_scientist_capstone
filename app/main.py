from flask import Flask, render_template, request, jsonify
from data import get_clean_ticker_data
from graph import generate_line_graph_json

app = Flask(__name__)

# Define the supported tickers
TICKERS = ['AAPL','GOOG','MSFT']


@app.route('/', methods=["GET"])
def home():
    """
    Displays the homepage.
    """

    return render_template('home.html', ticker_options=TICKERS)

@app.route('/', methods=['POST'])
def process_request():
    print(request)

    ticker_symbol = request.form.get('ticker_symbol',None)

    df = get_clean_ticker_data(ticker_symbol)
    ticker_table = df.tail(10).loc[:,['adj_close']].T.to_html() ## TODO: turn this into a proper table

    line_graphJSON = generate_line_graph_json(df, ticker_symbol)

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