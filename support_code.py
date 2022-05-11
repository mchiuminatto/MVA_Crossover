import pandas as pd
import numpy as np
from scipy.stats import norm
import scipy
import talib as ta
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn as sns, numpy as np
sns.set_theme(style="whitegrid")
import mplfinance as mpf

class BlockBootStrapSamp:

    """
    Block bootstrap sampling with overlapping for time series

    """

    def __init__(self, dec_places:int = 2):
        
        self.dec_places = dec_places

        self.mean_sampling: pd.Series = None
        self.samplinpipg_mean: float = None
        self.sampling_median: float = None
        self.sampling_std: float = None
        self.sampling_std_error: float = None
        self.sampling_min: float = None
        self.sampling_max: float = None

    def __str__(self):
        return f""" sampling mean: {self.sampling_mean}, 
                    sampling median: {self.sampling_median}
                    sampling std: {self.sampling_std}, 
                    sampling standard error: {self.sampling_std_error},
                    sampling min: {self.sampling_min},
                    sampling_max: {self.sampling_max}"""

    def compute(self, data: pd.Series, sample_size: int):
        # syntactic sugar
        
        k = sample_size
        n = len(data)
        
        # bootstrapping sampling process
        total_samples = n - k + 1
        # print("Expected samples ", total_samples)
        self.mean_sampling = data.rolling(k).mean()
        self.mean_sampling.dropna(inplace=True)
        # print("Samples ", len(self.mean_sampling))
        if total_samples != len(self.mean_sampling):
            raise Warning("Expected number of samples differs from actual number of samples")
        
        # stats calculations
        self.sampling_mean = self.mean_sampling.mean().round(self.dec_places)
        self.sampling_median = self.mean_sampling.median().round(self.dec_places)
        self.sampling_std = self.mean_sampling.std().round(self.dec_places)
        self.sampling_std_error = scipy.stats.sem(self.mean_sampling).round(self.dec_places)
        self.sampling_min = round(min(self.mean_sampling), self.dec_places)
        self.sampling_max = round(max(self.mean_sampling), self.dec_places)


class ConfidenceInterval:

    def __init__(self, dec_places:int = 2):
        
        self.dec_places: int = dec_places
        self.ci_left: float = None
        self.ci_right: float = None
        self.mean: float = None
        self.std_err: float = None

    def __str__(self):
        return f"confidence interval: [{self.ci_left}, {self.ci_right}], mean: {self.mean}, standard error: {self.std_err}"

    def compute(self, alpha: float, mean: float, std_error: float ):
            assert 0 <= alpha <= 1, "Alpha must be in the range [0, 1]"
            self.mean = mean
            self.std_err = std_error

            cl = 1 - alpha
            ci = scipy.stats.norm.interval(cl, loc=mean, scale=std_error)
            self.ci_left = round(ci[0], self.dec_places)
            self.ci_right = round(ci[1], self.dec_places)

            
class PlotDistribution:

    def plot(self, sample_data: pd.Series, sample_min: float, sample_max: float,  sample_mean: float, sample_median: float, sample_std_dev: float):

        
        # plot distwith normal, std_error: float curce as reference

        x = np.linspace(sample_min, sample_max, 100)
        D = scipy.stats.norm.pdf(x, loc=sample_mean, scale=sample_std_dev)

        fig, axis=plt.subplots(1,1, figsize=(6,3))
        sample_data.hist(grid=False, bins=20, density=True)
        plt.plot([sample_mean, sample_mean], [0, max(D)], color='g', linestyle='--', label='mean')
        plt.plot([sample_median, sample_median], [0, max(D)], color='orange', linestyle='--', label='median')
        plt.plot(x,D, color="r", label="Normal distrib.")
        plt.legend(fontsize=8)
        plt.title('Profit distribution', size=15)
        plt.show()


