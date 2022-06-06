import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging


class Metrics:

    def __init__(self, date_col="date", return_col="RETURN", pl_col="PL", ann_risk_free_ret=0.02):

        self.date_col = date_col
        self.return_col = return_col
        self.pl_col = pl_col
        self.ann_risk_free_ret = ann_risk_free_ret

        self.metrics = {
            "Sortino Ratio": 0,
        }

    def calc_tot_profit(self, df):
        self.metrics["Total Profit"] = df[self.pl_col].sum()

    def calc_ann_return(self, df):

        """
        Calculate annualized return average

        ann = SUM()/(# years)

        :param df:
        :return:
        """
        _years = df[self.date_col].dt.year.unique()
        _n_years = len(_years)
        _tot_return = df[self.return_col].sum()
        _ann_return = (pow((1 + _tot_return), (1/_n_years)) - 1)

        self.metrics["Annual Return %"] = np.round(_ann_return, 5)

    def calc_distrib_moments(self, df, freq="M"):

        _df_res = df.resample(freq).sum()
        self.metrics[f"Kurtosis {freq}"] = np.round(_df_res[self.return_col].kurtosis(), 6)
        self.metrics[f"Skewness {freq}"] = np.round(_df_res[self.return_col].skew(), 6)
        self.metrics[f"Stdev {freq}"] = np.round(_df_res[self.return_col].std(), 6)

    def calculate_max_dd(self, df):
        _dd_vctor = Profits.max_dd(df, self.pl_col, True)
        self.metrics["Max DD %"] = np.round(100*_dd_vctor[0], 2)

    def calculate_sharpe(self, df, rf_ret_ann):
        _sr = Sharpe()
        self.metrics["Sharpe ratio (yearly)"] = np.round(_sr.compute(df[self.return_col], rf_ret_ann, "Y"), 6)
        self.metrics["Sharpe ratio (monthly)"] = np.round(_sr.compute(df[self.return_col], rf_ret_ann, "M"), 6)
        self.metrics["Sharpe ratio (quarterly)"] = np.round(_sr.compute(df[self.return_col], rf_ret_ann, "Q"), 6)
        self.metrics["Sharpe ratio (weekly)"] = np.round(_sr.compute(df[self.return_col], rf_ret_ann, "W"), 6)

    def calculate_winning_stats(self, df, freq="M"):
        _df_resamp = df.resample("M").sum()

        tot_months = len(_df_resamp)
        mask_positive = _df_resamp[self.return_col] > 0
        pos_month = len(_df_resamp[mask_positive])
        self.metrics["Positive months %"] = np.round(100*(pos_month / tot_months), 2)

        self.metrics["Avg. profit winning months"] = np.round(_df_resamp[mask_positive][self.return_col].mean(), 6)
        self.metrics["Avg. profit losing months"] = np.round(_df_resamp[~mask_positive][self.return_col].mean(), 6)

    def calculate_average_trades(self, df, freq="M"):
        _df_resamp = df.resample("W").count()
        self.metrics["Avg. trades/week"] = np.round(_df_resamp.iloc[:, 0].mean(), 3)

    def save_metrics(self, folder, file_name):
        df_metrics = pd.DataFrame.from_dict(self.metrics, orient="index")
        df_metrics.to_csv(f"{folder}{file_name}")

    def compute(self, df):

        self.calc_ann_return(df)
        self.calculate_max_dd(df)
        self.calculate_sharpe(df, self.ann_risk_free_ret)
        self.calc_distrib_moments(df, "M")
        self.calculate_winning_stats(df, "M")
        self.calculate_average_trades(df, "W")


class Return:

    """
    Deprecated class only used by one module
    """

    def __init__(self, date_col="DATE",
                 capital_col="CAPITAL",
                 return_col="RETURN",
                 pl_col="PL"):

        self.date_col = date_col
        self.capital_col = capital_col
        self.return_col = return_col
        self.pl_col = pl_col


    def ret_over_initial_K(self, value: pd.Series):
        """
        Calculates return over a fix amount named initial capital

        :param value: Time Series of values over which the return will be calculated. Could be price,
        profit, or any other value
        :return:
        """

    def compute(self, df, pl, initial_capital):

        df[self.capital_col] = df[pl].cumsum() + initial_capital
        # df[self.return_col] = ( df[self.capital_col] - df[self.capital_col].shift(1) ) / df[self.capital_col].shift(1)
        df[self.return_col] = ( df[self.capital_col] - df[self.capital_col].shift(1) ) / initial_capital
        index_0 = df.head(1).index
        df.loc[index_0, self.return_col] = (df.loc[index_0, self.capital_col] - initial_capital) / initial_capital
        df[self.return_col] = np.round(100*df[self.return_col], 6)


class Returns:
    """
    Different modes of returns calculations:

    * STD: Standard as defined in financial.
    * ROIV: Return over initial value, as requested by a particular customer.

    """

    def __init__(self):
        pass

    @staticmethod
    def ret_over_initial_K(values: pd.Series, initial_value: float, shift_back: int = 1) -> pd.Series:
        """
        Calculates return over a fix amount named initial capital.

        Ret(i) = (v(i) - v(i-shift_back)/initial_capital)

        This mode of returns calculation is named ROIV: Return over initial value

        :param values: Time Series of values over which the return will be calculated. Could be price,
        profit, or any other value
        :param initial_value: Initial value for the return series. Could be initial capital or any other value
        :param shift_back: number of periods to the oldest value for calculation is shifted back

        :return:
        _returns: Time Series with calculated returns

        """

        values.iloc[0] = values.iloc[0] + initial_value
        _cum_sum = values.cumsum()
        _returns = (_cum_sum - _cum_sum.shift(shift_back)) / initial_value
        return _returns

    @staticmethod
    def ret_standard(values: pd.Series, initial_value: float, shift_back: int = 1) -> pd.Series:
        """
        Performs the standard calculation for returns as follows:
        R(i) = (values(i) - values(shift_back)) / values(shift_back)

        This runs under mode STD (Standard Calculation)

        :param values: Time Series of values over which the return will be calculated. Could be price,
        profit, or any other value
        :param initial_value: Initial value for the return series. Could be initial capital or any other value
        :param shift_back: number of periods to the oldest value for calculation is shifted back
        :return:
        """

        tmp_val = values.copy(deep=True)
        tmp_val.iloc[0] = tmp_val.iloc[0] + initial_value
        _cum_sum = tmp_val.cumsum()
        _returns = (_cum_sum - _cum_sum.shift(shift_back))/_cum_sum.shift(shift_back)
        return _returns

    def compute(self, values: pd.Series, initial_value: float, shift_back: int = 1, mode="STD"):
        """
        Coordinates returns calculation based on mode: STD or ROIV

        :param values: Time Series of values over which the return will be calculated. Could be price,
        :param initial_value: Initial value for the return series. Could be initial capital or any other value
        :param shift_back: number of periods to the oldest value for calculation is shifted back
        :param mode: Indicates if the calculation mode is standard "STD" (default) or return over initial value (ROIV)
        :return:
            _returns: Time Series with returns calculation
        """

        if mode in ["STD", "std", "standard"]:
            _returns = self.ret_standard(values, initial_value, shift_back=shift_back)
        elif mode in ["ROIV", "roiv"]:
            _returns = self.ret_over_initial_K(values, initial_value, shift_back=shift_back)
        else:
            raise Exception(f"Mode {mode} is not valid. Modes must be STD or ROIV")

        return _returns


class DrawDown:

    def __init__(self, plot=True):
        self.results = dict()
        self.plot = plot

    def compute(self, profits, initial_capital=0, plot=True):
        """
        Calculates the maximum draw down for a profit series

        :param profits: Time Series with profits or return values
        :param initial_capital: Initial capital
        :param plot: Plot (True) or not (False)

        :return
        * dd: Maximum draw down <br>
        * min_cum: accumulated profit at the bottom of draw down<br>
        * max_cum: cumulated profit at the top of the draw down<br>
        * delta: difference in pips for between the maximum draw down and minimum draw dawn<br>
        * pf_dd: Is the profit draw down ratio _pft/(_max_cum - _min_cum): Profit height / DD height.
        """
        self.results["dd"] = -1
        self.results["min_cum"] = -1
        self.results["max_cum"] = -1
        self.results["delta"] = -1

        try:
            if len(profits) == 0:
                # empty input_currency dataset
                return 0, 0, 0, 0, 0
            _tmp_pft = profits.copy(deep=True)
            # _tmp_pft.dropna(inplace=True)
            # _tmp_pft.reset_index(inplace=True)
            _tmp_pft.fillna(0, inplace=True)
            _tmp_pft.iloc[0] = _tmp_pft.iloc[0] + initial_capital
            xs = _tmp_pft.cumsum().values
            i = np.argmax(np.maximum.accumulate(xs) - xs)  # end of the period

            if len(xs) == 0:
                # empty input_currency data set
                logging.warning("Empty input in DD calculation")
                return 0, 0, 0, 0, 0

            if len(xs[:i]) == 0:
                # not enough data to process calculate draw down.
                logging.warning("Not enough data for DD calculation ", len(xs[:i]))
                return 0, 0, 0, 0, 0

            j = np.argmax(xs[:i])  # start of period
            if plot:
                plt.plot(xs)
                plt.plot([i, j], [xs[i], xs[j]], 'o', color='Red', markersize=10)
                plt.show()

            _pft = profits.sum()

            _min_cum = xs[i]
            _max_cum = xs[j]
            _dd = np.abs((_max_cum - _min_cum) / (_max_cum + 1E-8))
            _delta = np.abs(_max_cum - _min_cum)

            _pft_dd = max(0, (_pft) / (_delta + 1E-8))
        except Exception as e:
           logging.error(f"Calculating draw down - " + str(e))
           return 0, 0, 0, 0, 0

        self.results["dd"] = _dd
        self.results["min_cum"] = _min_cum
        self.results["max_cum"] = _max_cum
        self.results["delta"] = _delta
        self.results["pft_dd"] = _pft_dd


class Sharpe():
    PERIODS_ANNUM = {"M": 12,
                     "Y": 1,
                     "W": 52,
                     "Q": 4}

    def __init__(self):
        self.results = dict()


    def compute(self, return_col, avg_annual_rf, period):
        """
        Calculates sharpe ratio as follows, considering
        an average annualized risk free return

        Sharpe = (R - Rf)/stdev(RX)

        :param return_col: Return column
        :param avg_annual_rf: Annualized risk free ratio
        :param period: Y: yearly, M: monthly, W: weekly
        :return:
        """

        # resample

        assert period.upper() in ["Y", "M", "W", "Q"], "period must be one of the following values Y, M, W, Q"

        return_col.fillna(0, inplace=True)
        _ret_period_rsmpl = return_col.resample(period).sum()

        # period adjusted risk_free return
        _rf_ret_rate = avg_annual_rf / self.PERIODS_ANNUM[period.upper()]

        # calculate sharpe ratio

        _ret_stdev = _ret_period_rsmpl.std()
        _ret_avg = _ret_period_rsmpl.mean()
        self.results["sharpe_ratio"] = (_ret_avg - _rf_ret_rate)/_ret_stdev

        print("SHARPE", self.results["sharpe_ratio"], _ret_avg, _rf_ret_rate, _ret_stdev)


class Sortino():

    def __init__(self):
        self.calcs = dict()

    def compute(self, return_col, ann_tgt_ret):

        _tgt_ret = ann_tgt_ret
        _ret_resamp = return_col.resample("M").sum()

        _n_months = len(_ret_resamp)
        _excess_ret = 0
        _excess_ret = (_ret_resamp - ann_tgt_ret)
        _avg_exret = _excess_ret.mean()
        self.calcs["Avg. Excess Return"] = _avg_exret

        _mask = (_ret_resamp - ann_tgt_ret) < 0
        #_excess_ret.loc[_mask] = (_ret_resamp[_mask] - ann_tgt_ret)
        _moment_2d = (_ret_resamp[_mask] - ann_tgt_ret).pow(2).sum()
        _avg_ret = _ret_resamp[_mask].mean()

        if _moment_2d < 0:
            return np.nan

        _dwn_rsk = np.sqrt(_moment_2d/_n_months)
        if _dwn_rsk == 0:
            return  np.nan

        self.calcs["Downside risk"] = _dwn_rsk
        _sortino = (_avg_ret - ann_tgt_ret)/_dwn_rsk

        return _sortino


class Profits:

    DESC_MAP = {}
    


    def __init__(self, net_pft_col="net_profit_pips", 
                 cum_pft_col = "acc_profit_pips", 
                 gross_profit_col="gross_profit", 
                 init_capital=10_000):

        self.net_pft_col = net_pft_col
        self.cum_pft_col = cum_pft_col
        self.gross_pft_col = gross_profit_col
        self.init_capital = init_capital

        self.metrics = dict()
        self.build_description_map()

        

    def build_description_map(self):    
        self.DESC_MAP[self.net_pft_col] = "Net Profit"
        self.DESC_MAP[self.gross_pft_col] = "Gross Profit"


        self.DESC_MAP["total_trades"] = "Total trades"
        self.DESC_MAP["winning_trades"] = "Winning trades"
        self.DESC_MAP["losing_trades"] = "Losing tradest"
        self.DESC_MAP["avg_winning"] = "Average winning profit"
        self.DESC_MAP["avg_losing"] = "Average losing profit"
        self.DESC_MAP["avg_profit"] = "Average profit"

        self.DESC_MAP["total_pl"] = "Total profit&loss"
        self.DESC_MAP["total_profit"] = "Total profit"
        self.DESC_MAP["total_loss"] = "Total loss"
        self.DESC_MAP["stdev_pl"] = "Profit & loss std. deviation"
        self.DESC_MAP["median_profit"] = "Median profit&loss"        
        self.DESC_MAP["skrew_pl"] = "Skew profit & loss"        

    def metris_description(self):
        _metrics_dict = {self.DESC_MAP[k]:self.metrics[k] for k in self.DESC_MAP.keys()}
        return _metrics_dict

    def calc_net_profit(self, df, cost):
        """
        Calculates the trade profit and accumulative profit from
        gross profit (in pips) column which is already calculated.

        net_profit_pip = pip_change - cost
        acc_profit_pip = cumsum(net_profit_pip)
        :param df:
        :param cost:
        :return:
        """

        df[self.net_pft_col] = df[self.gross_pft_col] - cost
        df[self.cum_pft_col] = df[self.net_pft_col].cumsum().astype(float)


    def calc_metrics(self, df):
        """
        Calculates a set of  metrics:

        Basic set

        Total trades (total_trades)
        Winner trades (winning_trades)
        Loser trades (losing_trades)
        Total Profit and Loss (total_pl)
        Total Profit
        Total Loss
        Profit standard deviation
        Cumulative profit standard deviation
        Expected (mean) profit

        :param df:
        :return:
        """

        # basic set
        _mask_win = (df[self.net_pft_col] > 0)
        self.metrics["total_trades"] = len(df)
        self.metrics["winning_trades"] = len(df[_mask_win])
        self.metrics["losing_trades"] = len(df[~_mask_win])
        self.metrics["avg_winning"] = df[_mask_win]["net_profit"].mean()
        self.metrics["avg_losing"] = df[~_mask_win]["net_profit"].mean()
        self.metrics["total_pl"] = df[self.net_pft_col].sum()
        self.metrics["total_profit"] = df[_mask_win][self.net_pft_col].sum()
        self.metrics["total_loss"] = df[~_mask_win][self.net_pft_col].sum()
        self.metrics["stdev_pl"] = df[self.net_pft_col].std(0)
        self.metrics["stdev_cum_pl"] = df[self.cum_pft_col].std(0)
        self.metrics["avg_profit"] =  df[self.net_pft_col].mean()
        self.metrics["median_profit"] =  df[self.net_pft_col].median()
        self.metrics["skew_pl"] = df["net_profit"].skew()


    def compute(self, df, cost):

        self.calc_net_profit(df, cost)
        self.calc_metrics(df)