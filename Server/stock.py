import pandas as pd
import numpy as np
import yfinance as yf
import datetime

class Stock:
    def __init__(self, tck, tf):
        self.ticker_name = tck
        self.ticker = yf.Ticker(tck)

        self.stock_info = self.ticker.info
        self.df = self.ticker.history(period="2y", interval=tf)[['Open', 'High', 'Low', 'Close', 'Volume']].round(2)
        self.df["lastClose"] = self.df['Close'].shift(1)

        #self.financials = self.ticker.financials.rename(columns=lambda x: datetime.datetime.strftime(x, '%Y-%m-%d')).dropna()
        #self.financials = self.financials.to_dict()

        self.earnings = self.ticker.quarterly_earnings.to_dict()
        self.balance_sheet = self.ticker.balance_sheet.to_dict()
        print(self.balance_sheet)

        self.financials = {
            "earnings": self.earnings,
            # "balance_sheet": self.balance_sheet
        }

        self.balance_sheet = self.ticker.balance_sheet

        self.emas_calcul()
        self.pivot_calcul()
        self.return_statistics = self.return_stats()
        self.gap_statistics = self.gap_stats()

        self.df = self.df.iloc[-200:].round(4)

        self.df['ts'] = self.df.index.values.astype(np.int64) // 10 ** 9 * 1000
        self.data_json_friendly = self.df.reset_index().to_dict(orient="records")
    

    def pivot_calcul(self):
        self.df['pp'] = (self.df['High'].shift(1)+self.df['Low'].shift(1)+self.df['Close'].shift(1))/3
        self.df['s1'] = 2*self.df['pp'] - self.df['High']
        self.df['s2'] = self.df['pp'] - (self.df['High']-self.df['Low'])
        self.df['r1'] = 2*self.df['pp'] - self.df['Low']
        self.df['r2'] = self.df['pp'] + (self.df['High'] - self.df['Low'])


    def emas_calcul(self):
        ema_tf = [9,12,20,50,100,200]

        for i in ema_tf:
            self.df['ema' + str(i)] = self.df['Close'].ewm(span=i).mean().round(2)


    def return_stats(self):
        self.df["return"] = self.df["Close"]/self.df["Open"]-1
        self.df['return'] = self.df["return"].round(6)

        r_mean = self.df["return"].mean()
        r_median = self.df["return"].median()
        r_25 = self.df["return"].quantile(0.25)
        r_75 = self.df["return"].quantile(0.75)
        r_max = self.df["return"].max()
        r_min = self.df["return"].min()

        r_dict = {"Mean": r_mean, "Median": r_median,"25%": r_25,"75%": r_75, "Min": r_min, "Max": r_max}

        return r_dict


    def gap_stats(self):
        gap = self.df.loc[abs(self.df["Open"]/self.df["lastClose"]-1)>0.01]
        up_gap = gap.loc[gap['Open']>gap['lastClose'].shift(-1)]
        down_gap = gap.loc[gap['Open']<gap['lastClose'].shift(-1)]

        up_gap_count_percent = len(up_gap)/len(self.df) if len(self.df)>0 else 0
        down_gap_count_percent = len(down_gap)/len(self.df) if len(self.df)>0 else 0

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

    def api_result(self):
        res_dict = {
            "info":self.stock_info, 
            "returnStatistics":self.return_statistics, 
            "prices":self.data_json_friendly, 
            "gapStatistics":self.gap_statistics, 
            "financials":self.financials
        }
        return res_dict


    def __repr__(self):
        return repr(self.df)


# x = Stock('btc-eur', '1d')
# print(x)