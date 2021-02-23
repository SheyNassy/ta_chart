import urllib.request
import json
import numpy as np
import pandas as pd
import mplfinance as mpf

from OhclvTA import OhclvTechnicalAnalyzeCalculator


def get_url():
    return "https://query1.finance.yahoo.com/v8/finance/chart/%5EN225?symbol=%5EN225&period1=1577854845&period2=1614053083&interval=1d"


print("Start")
str_url = get_url()
readObj = urllib.request.urlopen(str_url)
response = readObj.read()
ohlcv_json = json.loads(response)
ohlcv_df = pd.DataFrame(np.array(ohlcv_json["chart"]["result"][0]["timestamp"]),
                        columns=["Timestamp"])
ohlcv_df["Timestamp"] = pd.to_datetime(ohlcv_df['Timestamp'].astype(int), unit='s')
ohlcv_df["Open"] = np.array(ohlcv_json["chart"]["result"][0]["indicators"]["quote"][0]["open"]).astype(float)
ohlcv_df["High"] = np.array(ohlcv_json["chart"]["result"][0]["indicators"]["quote"][0]["high"]).astype(float)
ohlcv_df["Low"] = np.array(ohlcv_json["chart"]["result"][0]["indicators"]["quote"][0]["low"]).astype(float)
ohlcv_df["Close"] = np.array(ohlcv_json["chart"]["result"][0]["indicators"]["quote"][0]["close"]).astype(float)
ohlcv_df["Volume"] = np.array(ohlcv_json["chart"]["result"][0]["indicators"]["quote"][0]["volume"]).astype(float)

# 本家のほうがDataFrame渡しになったら変える
ohlcv_df = OhclvTechnicalAnalyzeCalculator.calc(ohlcv_df.values.tolist())
ohlcv_df.to_csv("hoge.csv")

# DateTime列をIndexにする
ohlcv_df = ohlcv_df.set_index('Timestamp')

#
apd_oscilator = [
    mpf.make_addplot(ohlcv_df["BbH"], panel=0),
    mpf.make_addplot(ohlcv_df["BbM"], panel=0),
    mpf.make_addplot(ohlcv_df["BbL"], panel=0),
    mpf.make_addplot(ohlcv_df["StdDev"], panel=1),
    mpf.make_addplot(ohlcv_df["Adx"], panel=1),
    ]
# 描画(https://saturday-in-the-park.netlify.app/TradingTools/06_PlotDailyChart/)
mpf.plot(ohlcv_df, type='candle', style='yahoo',  addplot=apd_oscilator)


print("End")
