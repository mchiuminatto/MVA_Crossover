import pandas as pd
class Signal:
    """
    Simple trading signal marking, based on pre-defined entry and exit conditions
    
    """
    
    def __init__(self, signal_col = "signal"):
        self.signal_col = signal_col

    def compute(self, df: pd.DataFrame, entry_sig_cond: pd.Series, exit_sig_cond: pd.Series) -> pd.Series:
        """
        Marks entry and exist signals based on vectorial conditions 
        passed as parameters.
        The signal is assigned in a new column with name "signal.col_name" and 
        is returned (even though is included in the original data set)
    

        Parameters:
        * df: dataset where to create the column
        * entry_sig_cod: Vectorized boolean entry condition
        * exit_sig_cod: Vectorized boolean exit condition

        Returns:

        * signal: series with the entry(1)/exit(-1) signal marked
        """

        
        if not (df.shape[0] == entry_sig_cond.shape[0]) or not (df.shape[0] == exit_sig_cond.shape[0]):
            raise ArithmeticError("Either the data set and signal condition vectors needs to be the same shape")

        df.loc[entry_sig_cond, self.signal_col] = 1
        df.loc[exit_sig_cond, self.signal_col] = -1

        return df[self.signal_col]


