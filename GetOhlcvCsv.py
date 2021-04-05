import urllib.request
import json
import numpy as np
import pandas as pd
import mplfinance as mpf
from OhclvTA import OhclvTechnicalAnalyzeCalculator
from datetime import datetime as dt


def get_url(MeigaraCode, DateTimeFrom, DateTimeTo, Piriod):
    datetime_from = dt.strptime(DateTimeFrom, '%Y-%m-%d')
    datetime_to = dt.strptime(DateTimeTo, '%Y-%m-%d')

    return "https://query1.finance.yahoo.com/v8/finance/chart/" + MeigaraCode \
           + "?symbol=" + MeigaraCode \
           + "&period1=" + str("{:.0f}".format(datetime_from.timestamp())) \
           + "&period2=" + str("{:.0f}".format(datetime_to.timestamp())) \
           + "&interval=" + Piriod


print("Start")
str_mei = "BTC-JPY"
# str_mei = "%5EN225"
str_dtf = dt(dt.today().year, dt.today().month - 3, 1).strftime('%Y-%m-%d')
str_dtt = dt.today().strftime('%Y-%m-%d')
str_url = get_url(str_mei, str_dtf, str_dtt, "1d")
str_csv = str_mei + "_" + str_dtf + "_" + str_dtt + ".csv"

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
ohlcv_df.to_csv("data\\" + str_csv, index=False)

# DateTime列をIndexにする
ohlcv_df = ohlcv_df.set_index('Timestamp')

#
apd_oscilator = [
    # mpf.make_addplot(ohlcv_df["Sma5"], panel=0),
    # mpf.make_addplot(ohlcv_df["TbpP"], panel=0, type='scatter', color='r'),
    # mpf.make_addplot(ohlcv_df["TbpM"], panel=0, type='scatter', color='b'),
    mpf.make_addplot(ohlcv_df["StdDev"], panel=1, color='g'),
    mpf.make_addplot(ohlcv_df["Adx"], panel=1, color='r'),
    mpf.make_addplot(ohlcv_df["SdBlaTp"], panel=2, type='bar', color='r', width=1),
    mpf.make_addplot(ohlcv_df["SdBlaTm"], panel=2, type='bar', color='b', width=1),
    mpf.make_addplot(ohlcv_df["SarTp"], panel=3, type='bar', color='r', width=1),
    mpf.make_addplot(ohlcv_df["SarTm"], panel=3, type='bar', color='b', width=1),
    mpf.make_addplot(ohlcv_df["MACycleT1"], panel=4, type='bar', color='#FF0000', width=1),
    # mpf.make_addplot(ohlcv_df["MACycleT2"], panel=4, type='bar', color='#000000', width=1),
    # mpf.make_addplot(ohlcv_df["MACycleT3"], panel=4, type='bar', color='#000000', width=1),
    mpf.make_addplot(ohlcv_df["MACycleT4"], panel=4, type='bar', color='#0000FF', width=1),
    # mpf.make_addplot(ohlcv_df["MACycleT5"], panel=4, type='bar', color='#000000', width=1),
    # mpf.make_addplot(ohlcv_df["MACycleT6"], panel=4, type='bar', color='#000000', width=1),
]
# 描画(https://saturday-in-the-park.netlify.app/TradingTools/06_PlotDailyChart/)
mpf.plot(ohlcv_df, type='candle', style='yahoo', addplot=apd_oscilator, datetime_format='%Y/%m/%d', xrotation=270)

print("End")
