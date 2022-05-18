import pandas as pd
import pytest 

from SignalLib.tests.TestPrep import TestPrep as tp

# tested modules
from SignalLib.Signal import Signal



def test_mismatching_shapes():
    # open data_set
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
    
    with pytest.raises(ArithmeticError) as exp:
        _sig_calc = _signal.compute(_df[10:], _entry_signal, _exit_signal)
        assert exp.value == "Either the data set and signal condition vectors needs to be the same shape"
