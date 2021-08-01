from flask import Flask, render_template, request, jsonify
from get_data import get_ticker_data, create_candle_json

app = Flask(__name__)

#templates = Jinja2Templates(directory="app/templates")

@app.route('/', methods=["GET"])
def home():
    """
    Displays the homepage.
    """
    return render_template('home.html')

@app.route('/', methods=['POST'])
def process_request():
    ticker_symbol = request.form.get('ticker_symbol', None)


    df = get_ticker_data(ticker_symbol)
    ticker_table = df.tail(10).loc[:,['adj_close']].T.to_html()

    graphJSON = create_candle_json(df, ticker_symbol)
    print(graphJSON[:50])

    return render_template('home.html', 
                           ticker_symbol=ticker_symbol,
                           ticker_table=ticker_table,
                           graphJSON=graphJSON
    )


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()