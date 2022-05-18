import pandas as pd

class TestPrep(object):

    # region constants
    DATA_SET = "EURUSD_Hourly_Bid_2021.csv"
    SIGNAL_REF = "signal_bench.csv"
    TRADES_REF = "trades_bench.csv"

    # sma calculation
    SMA_fast = 10
    SMA_med = 25
    SMA_slow = 50
    COL_f = f'SMA_{SMA_fast}'
    COL_m = f'SMA_{SMA_med}'
    COL_s = f'SMA_{SMA_slow}'

    DIGITS = 4  # pip position
    # endregion

    @staticmethod
    def data_prep() -> dict:
        """
        Loads the required data sets for:
        price data (data) 
        reference signal (signal) 
        reference trades (trades) 

        Returns:

        dict: dictionary with the three data sets: "data", "signal", "trades"

        """
        _df = pd.read_csv(f"./data/{TestPrep.DATA_SET}")
        _df['Time (UTC)'] = pd.to_datetime(_df['Time (UTC)']) 
        _df.set_index('Time (UTC)', inplace=True)
        # _df.sort_index(inplace=True)
        
        # signal baseline (reference)
        _sig = pd.read_csv(f"./data/{TestPrep.SIGNAL_REF}")
        _sig['Time (UTC)'] = pd.to_datetime(_sig['Time (UTC)'])
        _sig.set_index('Time (UTC)', inplace=True)
        # _sig.sort_index(inplace=True)
        

        # trades baseline
        _trd = pd.read_csv(f"./data/{TestPrep.TRADES_REF}")
        _trd['Time (UTC)'] = pd.to_datetime(_trd['Time (UTC)']) 
        _trd.set_index('Time (UTC)', inplace=True)
        # _trd.sort_index(inplace=True)

        # pack datasets
        _data_sets = {"data":_df, "signal": _sig, "trades":_trd}

        return _data_sets

    @staticmethod
    def calc_features(df: pd.DataFrame) -> pd.DataFrame:
        df[TestPrep.COL_f] = df['Close'].rolling(TestPrep.SMA_fast).mean()
        df[TestPrep.COL_m] = df['Close'].rolling(TestPrep.SMA_med).mean()
        df[TestPrep.COL_s] = df['Close'].rolling(TestPrep.SMA_slow).mean()
        return df
    