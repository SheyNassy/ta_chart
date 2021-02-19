import urllib.request
import json
import numpy as np
import pandas as pd
import mplfinance as mpf

from OhclvTA import OhclvTechnicalAnalyzeCalculator


def get_url():
    return "https://query1.finance.yahoo.com/v8/finance/chart/%5EN225?symbol=%5EN225&period1=1524153600&period2=1610598552&interval=1d"


print("Start")
str_url = get_url()
readObj = urllib.request.urlopen(str_url)
response = readObj.read()
ohlcv_json = json.loads(response)
ohlcv_df = pd.DataFrame(np.array(ohlcv_json["chart"]["result"][0]["timestamp"]),
                        columns=["Timestamp"])
ohlcv_df["Timestamp"] = pd.to_datetime(ohlcv_df['Timestamp'].astype(int), unit='s')
ohlcv_df["Open"] = np.array(ohlcv_json["chart"]["result"][0]["indicators"]["quote"][0]["open"]).astype(np.float)
ohlcv_df["High"] = np.array(ohlcv_json["chart"]["result"][0]["indicators"]["quote"][0]["high"]).astype(np.float)
ohlcv_df["Low"] = np.array(ohlcv_json["chart"]["result"][0]["indicators"]["quote"][0]["low"]).astype(np.float)
ohlcv_df["Close"] = np.array(ohlcv_json["chart"]["result"][0]["indicators"]["quote"][0]["close"]).astype(np.float)
ohlcv_df["Volume"] = np.array(ohlcv_json["chart"]["result"][0]["indicators"]["quote"][0]["volume"]).astype(np.float)

# 本家のほうがDataFrame渡しになったら変える
ohlcv_df = OhclvTechnicalAnalyzeCalculator.calc(ohlcv_df.values.tolist())

# DateTime列をIndexにする
ohlcv_df = ohlcv_df.set_index('Timestamp')

#
apd_oscilator = [
    mpf.make_addplot(ohlcv_df["Sma5"], panel=0),
    mpf.make_addplot(ohlcv_df["Sma20"], panel=0),
    mpf.make_addplot(ohlcv_df["Sma60"], panel=0),
    mpf.make_addplot(ohlcv_df["SicH"], panel=0),
    mpf.make_addplot(ohlcv_df["SicL"], panel=0),
    ]
# 描画(https://saturday-in-the-park.netlify.app/TradingTools/06_PlotDailyChart/)
mpf.plot(ohlcv_df, type='candle', addplot=apd_oscilator)

print("End")
