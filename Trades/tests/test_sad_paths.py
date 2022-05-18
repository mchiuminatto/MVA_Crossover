import pandas as pd
from Trades.Trades import MarkDiscontinuous
from Trades.tests import TestPrep
import numpy as np
import pytest

def test_shape_mismatch():

    _trades = MarkDiscontinuous()
    _context = TestPrep.TestPrep.data_prep()
    _df = _context["data"]
    _sig = _context["signal"]

    with pytest.raises(ValueError) as exp:
        _sig_calc = _trades.compute(_df[10:], _sig)
        assert exp.value == "Either the data set and signal vectors needs to be the same shape"






