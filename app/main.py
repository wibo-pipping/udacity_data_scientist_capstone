from flask import Flask, render_template, request, jsonify
from get_data import get_ticker_data, create_candle_json, create_bar_chart, create_line_chart

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    """
    Displays the homepage.
    """

    return render_template('home.html')

@app.route('/', methods=['POST'])
def process_request():
    ticker_symbol = request.form.get('ticker_symbol', None)
    ticker_symbol = 'AAPL' if not ticker_symbol else ticker_symbol ## temporary


    df = get_ticker_data(ticker_symbol)
    ticker_table = df.tail(10).loc[:,['adj_close']].T.to_html()

    line_graphJSON = create_line_chart(df, ticker_symbol)

    return render_template('home.html', 
                           ticker_symbol=ticker_symbol,
                           ticker_table=ticker_table,
                           line_graphJSON = line_graphJSON
    )


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()