import pandas as pd

from SignalLib.tests.TestPrep import TestPrep as tp


# tested modules
from SignalLib.Signal import Signal


def test_signal_calculation():
    # open data sets
    _datasets = tp.data_prep()
    _df = _datasets["data"]
    _df = tp.calc_features(_df)
    
    # build signal conditions
    _entry_signal = (_df['Close'] > _df[tp.COL_f]) & (_df['Open'] < _df[tp.COL_f]) & \
                    (_df[tp.COL_f] > _df[tp.COL_m]) &  (_df[tp.COL_m] > _df[tp.COL_s]) 

    _exit_signal =  (_df['Close'] < _df[tp.COL_m]) & (_df['Open'] >  _df[tp.COL_m])
    
    # compute signals
    _sig = _datasets["signal"]
    _signal = Signal()
    _sig_calc = _signal.compute(_df, _entry_signal, _exit_signal)
    _sig_calc_safe = pd.DataFrame(_sig_calc['2021-02-01':])
    _sig_safe = pd.DataFrame(_sig['2021-02-01':])

    # compare
    _sig_compare = _sig_calc_safe['signal'].equals(_sig_safe['signal'])

    assert _sig_compare

