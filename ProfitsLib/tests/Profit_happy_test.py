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
