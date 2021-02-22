import numpy as np
import pandas as pd
import talib as ta


class OhclvTechnicalAnalyzeCalculator():
    def calc(marketItem):
        # 生配列をnp DataFrameに変換
        df_ohclv = pd.DataFrame(marketItem,
                                columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        # https://akatak.hatenadiary.jp/entry/2019/11/23/220836

        h = np.array(df_ohclv['High'].fillna(method='ffill'))
        l = np.array(df_ohclv['Low'].fillna(method='ffill'))
        c = np.array(df_ohclv['Close'].fillna(method='ffill'))

        # Simple Moving Average 5
        df_ohclv['Sma5'] = ta.SMA(c, timeperiod=5)
        # Simple Moving Average 20
        df_ohclv['Sma20'] = ta.SMA(c, timeperiod=20)
        # Simple Moving Average 60
        df_ohclv['Sma60'] = ta.SMA(c, timeperiod=60)

        # Exponential Moving Average 5
        df_ohclv['Ema5'] = ta.EMA(c, timeperiod=5)
        # Exponential Moving Average 20
        df_ohclv['Ema20'] = ta.EMA(c, timeperiod=20)
        # Exponential Moving Average 40
        df_ohclv['Ema40'] = ta.EMA(c, timeperiod=40)

        # 標準偏差
        df_ohclv['StdDev'] = ta.STDDEV(c, timeperiod=26)

        # ADX(Average Directional Movement Index 平均方向性指数)
        df_ohclv['Adx'] = ta.ADX(h, l, c, timeperiod=14)

        # Bollinger Bands
        upperband, middleband, lowerband = ta.BBANDS(c, timeperiod=21, nbdevup=0.75, nbdevdn=0.75, matype=0)
        df_ohclv['BbH'] = upperband
        df_ohclv['BbM'] = middleband
        df_ohclv['BbL'] = lowerband

        # ATR(Average True Range)
        df_ohclv['Adx'] = ta.ATR(h, l, c, timeperiod=14)

        # SIC (期間中の最大と最小)
        df_ohclv["SicH"] = pd.Series(df_ohclv.Close).rolling(window=20).max()
        df_ohclv["SicL"] = pd.Series(df_ohclv.Close).rolling(window=20).min()



        # # Simple Moving Average 5
        # df_ohclv['Sma5'] = pd.Series(df_ohclv.Close).rolling(window=5).mean()
        # # Simple Moving Average 20
        # df_ohclv['Sma20'] = pd.Series(df_ohclv.Close).rolling(window=20).mean()
        # # Simple Moving Average 60
        # df_ohclv['Sma60'] = pd.Series(df_ohclv.Close).rolling(window=60).mean()
        #
        # # Exponential Moving Average 5
        # df_ohclv['Ema5'] = pd.Series(df_ohclv.Close).ewm(span=5).mean()
        # # Exponential Moving Average 20
        # df_ohclv['Ema20'] = pd.Series(df_ohclv.Close).ewm(span=20).mean()
        # # Exponential Moving Average 40
        # df_ohclv['Ema40'] = pd.Series(df_ohclv.Close).ewm(span=40).mean()
        #
        # # True Range
        # df_ohclv['Tr'] = np.max([df_ohclv.High - df_ohclv.Low,
        #                          (pd.Series(df_ohclv.Close).shift(1) - df_ohclv.High).abs(),
        #                          (pd.Series(df_ohclv.Close).shift(1) - df_ohclv.Low).abs()],
        #                         axis=0)
        # # Average True Range
        # df_ohclv["Atr"] = pd.Series(df_ohclv.Tr).rolling(window=7).mean()
        #
        # # SIC (期間中の最大と最小)
        # df_ohclv["SicH"] = pd.Series(df_ohclv.Close).rolling(window=20).max()
        # df_ohclv["SicL"] = pd.Series(df_ohclv.Close).rolling(window=20).min()
        #
        # # Wilder Volatility System Trend
        # df_ohclv["WVST"] = "None"
        #
        #
        #
        # # Stop And Reverse (SAR)

        return df_ohclv
