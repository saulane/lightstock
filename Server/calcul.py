import pandas as pd
import numpy as np
import yfinance as yf
import datetime

class Stock:
    def __init__(self, tck, tf):
        self.ticker_name = tck
        self.ticker = yf.Ticker(tck)

        self.stock_info = self.ticker.info
        self.hist = self.ticker.history(period="2y", interval=tf)[['Open', 'High', 'Low', 'Close', 'Volume']].round(2)
        self.hist["lastClose"] = self.hist['Close'].shift(1)

        #self.financials = self.ticker.financials.rename(columns=lambda x: datetime.datetime.strftime(x, '%Y-%m-%d')).dropna()
        #self.financials = self.financials.to_dict()

        self.balance_sheet = self.ticker.balance_sheet

        self.emas_calcul()
        self.pivot_calcul()
        self.return_statistics = self.return_stats()
        self.gap_statistics = self.gap_stats()

        self.hist = self.hist.iloc[-200:].round(4)

        self.hist['ts'] = self.hist.index.values.astype(np.int64) // 10 ** 9 * 1000
        self.data_json_friendly = self.hist.reset_index().to_dict(orient="records")
    

    def pivot_calcul(self):
        self.hist['pp'] = (self.hist['High'].shift(1)+self.hist['Low'].shift(1)+self.hist['Close'].shift(1))/3
        self.hist['s1'] = 2*self.hist['pp'] - self.hist['High']
        self.hist['s2'] = self.hist['pp'] - (self.hist['High']-self.hist['Low'])
        self.hist['r1'] = 2*self.hist['pp'] - self.hist['Low']
        self.hist['r2'] = self.hist['pp'] + (self.hist['High'] - self.hist['Low'])


    def emas_calcul(self):
        ema_tf = [9,12,20,50,100,200]

        for i in ema_tf:
            self.hist['ema' + str(i)] = self.hist['Close'].ewm(span=i).mean().round(2)


    def return_stats(self):
        self.hist["return"] = self.hist["Close"]/self.hist["Open"]-1
        self.hist['return'] = self.hist["return"].round(6)

        r_mean = self.hist["return"].mean()
        r_median = self.hist["return"].median()
        r_25 = self.hist["return"].quantile(0.25)
        r_75 = self.hist["return"].quantile(0.75)
        r_max = self.hist["return"].max()
        r_min = self.hist["return"].min()

        r_dict = {"Mean": r_mean, "Median": r_median,"25%": r_25,"75%": r_75, "Min": r_min, "Max": r_max}

        return r_dict


    def gap_stats(self):
        gap = self.hist.loc[abs(self.hist["Open"]/self.hist["lastClose"]-1)>0.01]
        up_gap = gap.loc[gap['Open']>gap['lastClose'].shift(-1)]
        down_gap = gap.loc[gap['Open']<gap['lastClose'].shift(-1)]

        up_gap_count_percent = len(up_gap)/len(self.hist) if len(self.hist)>0 else 0
        down_gap_count_percent = len(down_gap)/len(self.hist) if len(self.hist)>0 else 0

        up_gap_filled = up_gap.loc[up_gap['Low'] <= up_gap['lastClose']]
        down_gap_filled = down_gap.loc[down_gap['High'] >= down_gap['lastClose']]

        up_gap_filled_count_percent = len(up_gap_filled)/len(up_gap) if len(up_gap)>0 else 0
        down_gap_filled_count_percent = len(down_gap_filled)/len(down_gap) if len(down_gap)>0 else 0

        filterStatistics = ['25%', '50%', '75%', 'max', 'mean', 'min']
        up_gap_return_stats = up_gap['return'].describe()[filterStatistics].to_dict()
        down_gap_return_stats = down_gap['return'].describe()[filterStatistics].to_dict()

        data_dict = {
            "upGap":
                {
                    "occurence": round(up_gap_count_percent, 4),
                    "percentFilled": round(up_gap_filled_count_percent, 4),
                    "dayReturnStats": up_gap_return_stats
                },
            "downGap":
                {
                    "occurence": round(down_gap_count_percent, 4),
                    "percentFilled": round(down_gap_filled_count_percent, 4),
                    "dayReturnStats": down_gap_return_stats
                }
        }

        return data_dict


    def __repr__(self):
        return repr(self.hist)


# x = Stock('btc-eur', '1d')
# print(x)