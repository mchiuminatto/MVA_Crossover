from ProfitsLib.Profits import Profits
import logging

def test_instatiation():
    _pft = Profits()
    assert _pft.cum_pft_col ==  "acc_profit_pips"
    assert _pft.gross_pft_col ==  "gross_profit"
    assert _pft.net_pft_col ==  "net_profit_pips"
    assert _pft.init_capital == 10_000


def test_instantiation_named():
    _pft = Profits(cum_pft_col="cum_pft", gross_profit_col="gross_profit", net_pft_col="net_profit", init_capital=5_000)
    assert _pft.cum_pft_col ==  "cum_pft"
    assert _pft.gross_pft_col ==  "gross_profit"
    assert _pft.net_pft_col ==  "net_profit"
    assert _pft.init_capital == 5_000



def test_calc_net_profit(prepare_context):

    _context = prepare_context
    _df = _context["data_set"]
    _cost = _context["cost"]
    _pft = Profits(net_pft_col="net_profit", gross_profit_col="gross_profit")
    _pft.calc_net_profit(_df, _cost)

    _total_trades = len(_df)
    _expected_net = _df[_pft.gross_pft_col].sum() - _cost * _total_trades
    _actual_net = _df[_pft.net_pft_col].sum()
    logging.info(f"Calculated net profit {_actual_net}  Expected net profit  {_expected_net}")
    assert _expected_net.round(2) == _actual_net.round(2)


def test_calc_metrics(prepare_context):

    _context = prepare_context
    _df = _context["data_set"]
    _cost = _context["cost"]
    _pft = Profits(net_pft_col="net_profit", gross_profit_col="gross_profit")
    _pft.calc_net_profit(_df, _cost)
    _pft.calc_metrics(_df)

    _exp_total_trades = len(_df)
    _exp_winning_trades = len(_df[(_df["net_profit"]>0)])
    _exp_losing_trades = len(_df[(_df["net_profit"]<=0)])
    _exp_pl = _df["net_profit"].sum().round(2)
    _exp_profit = _df[(_df["net_profit"]>0)]["net_profit"].sum().round(2)
    _exp_loss = _df[(_df["net_profit"]<=0)]["net_profit"].sum().round(2)
    _exp_stdev_pl = _df["net_profit"].std().round(2)
    _exp_stdev_cum_pl = _df["acc_profit_pips"].std().round(2)
    _exp_avg_pl = _df["net_profit"].mean().round(2)
    _exp_median_pft = _df["net_profit"].median().round(2)
  
    assert _exp_total_trades == _pft.metrics["total_trades"]
    assert _exp_winning_trades == _pft.metrics["winning_trades"]
    assert _exp_losing_trades == _pft.metrics["losing_trades"]
    assert _exp_pl == round(_pft.metrics["total_pl"], 2)
    assert _exp_profit == round(_pft.metrics["total_profit"], 2)
    assert _exp_loss == round(_pft.metrics["total_loss"], 2)
    assert _exp_stdev_pl == round(_pft.metrics["stdev_pl"], 2)
    assert _exp_stdev_cum_pl == round(_pft.metrics["stdev_cum_pl"], 2)
    assert _exp_avg_pl == round(_pft.metrics["avg_profit"], 2)
    assert _exp_median_pft == round(_pft.metrics["median_profit"], 2)


def test_compute(prepare_context):

    _context = prepare_context
    _df = _context["data_set"]
    _cost = _context["cost"]
    _pft = Profits(net_pft_col="net_profit", gross_profit_col="gross_profit")

    _pft.compute(_df, _cost)
    
    _exp_total_trades = len(_df)
    _exp_winning_trades = len(_df[(_df["net_profit"]>0)])
    _exp_losing_trades = len(_df[(_df["net_profit"]<=0)])
    _exp_pl = _df["net_profit"].sum().round(2)
    _exp_profit = _df[(_df["net_profit"]>0)]["net_profit"].sum().round(2)
    _exp_loss = _df[(_df["net_profit"]<=0)]["net_profit"].sum().round(2)
    _exp_stdev_pl = _df["net_profit"].std().round(2)
    _exp_stdev_cum_pl = _df["acc_profit_pips"].std().round(2)
    _exp_avg_pl = _df["net_profit"].mean().round(2)
    _exp_median_pft = _df["net_profit"].median().round(2)
  
    assert _exp_total_trades == _pft.metrics["total_trades"]
    assert _exp_winning_trades == _pft.metrics["winning_trades"]
    assert _exp_losing_trades == _pft.metrics["losing_trades"]
    assert _exp_pl == round(_pft.metrics["total_pl"], 2)
    assert _exp_profit == round(_pft.metrics["total_profit"], 2)
    assert _exp_loss == round(_pft.metrics["total_loss"], 2)
    assert _exp_stdev_pl == round(_pft.metrics["stdev_pl"], 2)
    assert _exp_stdev_cum_pl == round(_pft.metrics["stdev_cum_pl"], 2)
    assert _exp_avg_pl == round(_pft.metrics["avg_profit"], 2)
    assert _exp_median_pft == round(_pft.metrics["median_profit"], 2)


