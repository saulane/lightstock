from flask import Flask, jsonify, request, escape
from flask_cors import CORS
import yfinance as yf
import pandas as pd
from stock import Stock

#configuration
DEBUG = True

#instantier l'app
app = Flask(__name__)
app.config.from_object(__name__)

#CORS
CORS(app, ressources={r'*': {'origins':'*'}})


#check route
@app.route('/stocks/<stock_ticker>', methods=['GET'])
def stocks(stock_ticker):
    stk = Stock(escape(stock_ticker), "1d")

    return jsonify(stk.api_result())


if __name__ == '__main__':
    app.run()