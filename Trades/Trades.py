import pandas as pd
import numpy as np

class MarkDiscontinuous:

    def __init__(self, entry_exit_prd_col="en_ex_prd", 
                trade_col="trade", 
                trade_id_col="trade_id"):

        self.en_ex_prd_col = entry_exit_prd_col
        self.trade_col = trade_col
        self.trade_id_col = trade_id_col

    def compute(self, df: pd.DataFrame, signal: pd.Series) -> pd.DataFrame:

        # validations
        if df.shape[0] != signal.shape[0]:
            raise ValueError("Either the data set and signal vectors needs to be the same shape")

        # mark entry and exit bars
        df[self.en_ex_prd_col] = signal.shift(1)
       
        # mark trades
        df[self.trade_col] = df[self.en_ex_prd_col]
        df[self.trade_col].ffill(inplace=True)
        df[self.trade_col] =  df[self.trade_col].replace(-1, np.nan)

        # generate trades id

        # marks trade start
        mask_trade_start = (df[self.trade_col] == 1 ) & (df[self.trade_col].shift(1).isna())
        df.loc[mask_trade_start, self.trade_id_col] = range(1, len(df[mask_trade_start])+1)     
        df[self.trade_id_col].ffill(inplace=True)
        df.loc[df[self.trade_col].isna(), self.trade_id_col] = np.nan

        return df


