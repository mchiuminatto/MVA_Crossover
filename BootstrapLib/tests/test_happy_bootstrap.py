from BootstrapLib.Bootstrap import BlockBSWithOverlap
import pandas as pd

def test_bootstrapping(prepare_context):

    _context = prepare_context
    _data = _context["data"]
    
    _bstp = BlockBSWithOverlap()
    _bstp.compute(_data["Close"], 60)

    _check_df = _data.merge(_bstp.mean_sampling, how="left", left_index=True, right_index=True)
    _check_df["mean_sampling_check"] = _check_df["Close"].rolling(60).mean()

    assert (_check_df["mean_sampling_check"] - _check_df["sample_mean"]).sum() == 0
    assert _check_df[_check_df["sample_mean"].isna()].count()[0] == 59

   

    
    
