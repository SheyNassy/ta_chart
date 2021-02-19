import numpy as np
import pandas as pd

class OhclvTechnicalAnalyzeCalculator():
    def calc(marketItem):
        # 生配列をnp DataFrameに変換
        df_ohclv = pd.DataFrame(marketItem,
                                columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        # Simple Moving Average 5
        df_ohclv['Sma5'] = pd.Series(df_ohclv.Close).rolling(window=5).mean()
        # Simple Moving Average 20
        df_ohclv['Sma20'] = pd.Series(df_ohclv.Close).rolling(window=20).mean()
        # Simple Moving Average 60
        df_ohclv['Sma60'] = pd.Series(df_ohclv.Close).rolling(window=60).mean()

        # Exponential Moving Average 5
        df_ohclv['Ema5'] = pd.Series(df_ohclv.Close).ewm(span=5).mean()
        # Exponential Moving Average 20
        df_ohclv['Ema20'] = pd.Series(df_ohclv.Close).ewm(span=20).mean()
        # Exponential Moving Average 40
        df_ohclv['Ema40'] = pd.Series(df_ohclv.Close).ewm(span=40).mean()

        # True Range
        df_ohclv['Tr'] = np.max([df_ohclv.High - df_ohclv.Low,
                                 (pd.Series(df_ohclv.Close).shift(1) - df_ohclv.High).abs(),
                                 (pd.Series(df_ohclv.Close).shift(1) - df_ohclv.Low).abs()],
                                axis=0)
        # Average True Range
        df_ohclv["Atr"] = pd.Series(df_ohclv.Tr).rolling(window=7).mean()

        # SIC (期間中の最大と最小)
        df_ohclv["SicH"] = pd.Series(df_ohclv.Close).rolling(window=20).max()
        df_ohclv["SicL"] = pd.Series(df_ohclv.Close).rolling(window=20).min()

        # Wilder Volatility System Trend
        df_ohclv["WVST"] = "None"



        # Stop And Reverse (SAR)

        return df_ohclv