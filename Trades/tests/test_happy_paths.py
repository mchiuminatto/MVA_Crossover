# import logging
import pandas as pd
from Trades.Trades import MarkDiscontinuous
# import numpy as np


def test_instantiation_default():
    _test = MarkDiscontinuous(4)
    
    assert _test.pip_factor == 10000
    assert _test.entry_exit_period_col_name == "en_ex_prd"
    assert _test.trade_col_name == "trade"
    assert _test.trade_id_col_name == "trade_id"

def test_instantiation():
    _test = MarkDiscontinuous(4, entry_exit_period_col="enex_col", trade_col_name="trade_1",trade_id_col_name="tid1")
    
    assert _test.entry_exit_period_col_name == "enex_col"
    assert _test.trade_col_name == "trade_1"
    assert _test.trade_id_col_name == "tid1"

def test_mark_trades(data_prep):
    _trades_mark = MarkDiscontinuous(4)
    
    # prepare data and load reference data sets
    _data_sets: dict = data_prep
    _df: pd.DataFrame = _data_sets["data"]
    _signal: pd.Series = _data_sets["signal"]
    _trades: pd.DataFrame = _data_sets["trades"]
    
    _df = _trades_mark.mark_trades(_df, _signal)

    assert  _df.shape[0] == _trades.shape[0]
    assert _df[_trades_mark.trade_col_name].equals(_trades["trade"])
    assert _df[_trades_mark.entry_exit_period_col_name].equals(_trades["EN_EX_cond"])
    assert _df.iloc[0].name == _trades.iloc[0].name
    assert _df.iloc[-1].name == _trades.iloc[-1].name


def test_reduce_trades(data_prep):
    _trades_mark = MarkDiscontinuous(4)
    _data_sets: dict = data_prep

    _df: pd.DataFrame = _data_sets["data"]
    _signal: pd.Series = _data_sets["signal"]
    # _trades: pd.DataFrame = _data_sets["trades"]
    _digits: int = _data_sets["DIGITS"]

    _df_marked = _trades_mark.mark_trades(_df, _signal)

    _df_trades = _trades_mark.reduce_trades(_df_marked)

    for trade in _df_trades.iterrows():
        # logging.info(trade)
        _date_open = trade[1]["date_open"]
        _date_close = trade[1]["date_close"]
        _calc_gross_pft = trade[1]["gross_profit"]
        _expected_gross_pft = _df[_date_open:_date_close]["gross_profit"].sum()

        assert _calc_gross_pft - _expected_gross_pft < 10**-_digits
        
    
def test_trades_compute(data_prep):
    
    _trades_mark = MarkDiscontinuous(4)
    _data_sets: dict = data_prep

    _df: pd.DataFrame = _data_sets["data"]
    _signal: pd.Series = _data_sets["signal"]
    
    _df_marked = _trades_mark.mark_trades(_df, _signal)
    _df_trades = _trades_mark.reduce_trades(_df_marked)

    _df_trades_computed = _trades_mark.compute(_df, _signal)
    assert _df_trades_computed.equals(_df_trades)

    _df_trades.to_csv("trades_benchmark.csv")
