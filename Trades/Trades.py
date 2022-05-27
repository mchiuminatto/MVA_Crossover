import pandas as pd
import numpy as np


class MarkDiscontinuous:

    def __init__(self, 
                pip_decinmal_position: int,
                entry_exit_period_col: str="en_ex_prd", 
                trade_col_name: str="trade", 
                trade_id_col_name: str="trade_id"):

        if pip_decinmal_position is None:
            raise TypeError("Missing pip decimal position")

        self.pip_factor = 10**pip_decinmal_position
        self.entry_exit_period_col_name = entry_exit_period_col
        self.trade_col_name = trade_col_name
        self.trade_id_col_name = trade_id_col_name
        

    def mark_trades(self, df: pd.DataFrame, signal: pd.Series) -> pd.DataFrame:
        """
        Mark each trading period
        """

        # validations
        if df.shape[0] != signal.shape[0]:
            raise ValueError("Either the data set and signal vectors needs to be the same shape")

        # mark entry and exit bars
        df[self.entry_exit_period_col_name] = signal.shift(1)
       
        # mark trades
        df[self.trade_col_name] = df[self.entry_exit_period_col_name]
        df[self.trade_col_name].ffill(inplace=True)
        df[self.trade_col_name] =  df[self.trade_col_name].replace(-1, np.nan)

        # generate trades id
        _mask_trade_start = (df[self.trade_col_name] == 1 ) & (df[self.trade_col_name].shift(1).isna())

         # marks trade start
        df.loc[_mask_trade_start, self.trade_id_col_name] = range(1, len(df[_mask_trade_start]) + 1)     
        df[self.trade_id_col_name].ffill(inplace=True)
        df.loc[df[self.trade_col_name].isna(), self.trade_id_col_name] = np.nan

        return df

    def reduce_trades(self, df: pd.DataFrame):
        """
        Reduce trading periods to one record per trade
        """
        df['date'] = df.index
        _mask_trade = df[self.trade_id_col_name] > 0
        df.loc[_mask_trade, 'gross_profit'] = (df.loc[_mask_trade, 'Close'] - df.loc[_mask_trade, 'Open'] ) * self.pip_factor

        # reduction (aggregation) using groupby
        _df_trades_pft = df[[self.trade_id_col_name, 'gross_profit']].groupby(by=self.trade_id_col_name).sum()
        _df_trades_date = df[[self.trade_id_col_name, 'date']].groupby(by=self.trade_id_col_name).min()
        _df_trades_date_end = df[[self.trade_id_col_name, 'date']].groupby(by=self.trade_id_col_name).max()

        _df_trades = pd.merge(_df_trades_pft, _df_trades_date, how='inner', left_index=True, right_index=True)
        _df_trades = _df_trades.merge(_df_trades_date_end, how='inner', left_index=True, right_index=True, suffixes=["_open", "_close"])

        return _df_trades

    def compute(self, df: pd.DataFrame, signal: pd.Series) -> pd.DataFrame:
        # validations
        if df.shape[0] != signal.shape[0]:
            raise ValueError("Either the data set and signal vectors needs to be the same shape")

        df = self.mark_trades(df, signal)
        _df_trades = self.reduce_trades(df)

        return _df_trades
