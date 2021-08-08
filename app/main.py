from flask import Flask, render_template, request, jsonify
from get_data import get_ticker_data, generate_line_graph_json

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    """
    Displays the homepage.
    """
    tickers = ['AAPL','GOOG','MSFT']

    return render_template('home.html', ticker_options = tickers)

@app.route('/', methods=['POST'])
def process_request():
    ticker_symbol = request.form.get('ticker_symbol', None)
    ticker_symbol_dropdown = request.form.get('ticker_symbol_dropdown',None)

    if not ticker_symbol:
        ticker_symbol = ticker_symbol_dropdown

    df = get_ticker_data(ticker_symbol)
    ticker_table = df.tail(10).loc[:,['adj_close']].T.to_html()

    line_graphJSON = generate_line_graph_json(df, ticker_symbol)

    return render_template('home.html', 
                           ticker_symbol=ticker_symbol,
                           ticker_table=ticker_table,
                           line_graphJSON = line_graphJSON
    )


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()