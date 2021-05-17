from flask import Flask, jsonify, request, escape
from flask_cors import CORS
import yfinance as yf
import pandas as pd
from calcul import Stock

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
    # ticker = request.args["ticker"]
    stk = Stock(escape(stock_ticker), "1d")
    # print(stock_ticker)

    return jsonify(info=stk.stock_info, returnStatistics=stk.return_statistics, prices=stk.data_json_friendly, gapStatistics=stk.gap_statistics)


if __name__ == '__main__':
    app.run()