import pandas as pd
from scipy import stats

class BlockBSWithOverlap:

    """
    Block bootstrap sampling with overlapping for time series

    """

    def __init__(self, dec_places:int = 2):
        
        self.dec_places = dec_places
        self.mean_sampling: pd.Series = None
        self.sampling_median: float = None
        self.sampling_std: float = None
        self.sampling_std_error: float = None
        self.sampling_min: float = None
        self.sampling_max: float = None
        self.total_samples: int = None

    def __str__(self):
        return f""" sampling mean: {self.sampling_mean}, 
                    sampling median: {self.sampling_median}
                    sampling std: {self.sampling_std}, 
                    sampling standard error: {self.sampling_std_error},
                    sampling min: {self.sampling_min},
                    sampling max: {self.sampling_max}"""

    def compute(self, data: pd.Series, sample_size: int):
        # syntactic sugar
        k = sample_size
        n = len(data)
        
        # bootstrapping sampling process
        total_samples = n - k + 1
        # print("Expected samples ", total_samples)
        self.mean_sampling = data.rolling(k).mean()
        self.mean_sampling.dropna(inplace=True)
        self.mean_sampling.rename("sample_mean", inplace=True)
        # print("Samples ", len(self.mean_sampling))
        if total_samples != len(self.mean_sampling):
            raise Warning("Expected number of samples differs from actual number of samples")
        
        # stats calculations
        self.sampling_mean = self.mean_sampling.mean().round(self.dec_places)
        self.sampling_median = self.mean_sampling.median().round(self.dec_places)
        self.sampling_std = self.mean_sampling.std().round(self.dec_places)
        self.sampling_std_error = stats.sem(self.mean_sampling).round(self.dec_places)
        self.sampling_min = round(min(self.mean_sampling), self.dec_places)
        self.sampling_max = round(max(self.mean_sampling), self.dec_places)
        self.total_samples = total_samples
