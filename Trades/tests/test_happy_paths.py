import pandas as pd
from Trades.Trades import MarkDiscontinuous
from Trades.tests import TestPrep
import numpy as np

def test_instantiation_default():
    _test = MarkDiscontinuous()
    
    assert _test.en_ex_prd_col == "en_ex_prd"
    assert _test.trade_col == "trade"
    assert _test.trade_id_col == "trade_id"

def test_instantiation():
    _test = MarkDiscontinuous(entry_exit_prd_col="enex_col", trade_col="trade_1",trade_id_col="tid1")
    
    assert _test.en_ex_prd_col == "enex_col"
    assert _test.trade_col == "trade_1"
    assert _test.trade_id_col == "tid1"

def test_mark_trades():
    _trades_mark = MarkDiscontinuous()
    # prepare data and load refefence data sets
    _data_sets: dict = TestPrep.TestPrep.data_prep()
    _df: pd.DataFrame = _data_sets["data"]
    _signal: pd.Series = _data_sets["signal"]
    _trades: pd.DataFrame = _data_sets["trades"]
    
    _df = _trades_mark.compute(_df, _signal)

    assert  _df.shape[0] == _trades.shape[0]
    assert _df[_trades_mark.trade_col].equals(_trades["trade"])
    assert _df[_trades_mark.en_ex_prd_col].equals(_trades["EN_EX_cond"])
    assert _df.iloc[0].name == _trades.iloc[0].name
    assert _df.iloc[-1].name == _trades.iloc[-1].name



if __name__ == "__main__":
    test_mark_trades()
