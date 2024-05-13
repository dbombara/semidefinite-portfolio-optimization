import numpy as np
from tqdm import tqdm
import pandas as pd
from portfolio import Portfolio
import matplotlib.pyplot as plt
from constants import *

"""_summary_
0021ExpCardinality

"""
def main():
    i = 0 # loop counter
    var = K_vec # which variable are we testing?
    mean_time, std_time = np.zeros((len(var),)), np.zeros((len(var),))
    mean_returns, std_returns = np.zeros_like(mean_time), np.zeros_like(mean_time)
    m_obj, s_obj = np.zeros_like(mean_time), np.zeros_like(mean_time)
    mean_var, std_var = np.zeros_like(mean_time), np.zeros_like(mean_time)
    k_ = np.zeros_like(mean_time)

    for k in tqdm(var):
        df = df_.iloc[:,: ns]
        #
        ma = np.zeros((num_trials,))
        re = np.zeros((num_trials,))
        ov = np.zeros_like(re)
        vv = np.zeros_like(re)
        #
        for j in range(num_trials):
            p = Portfolio(stock_prices = df)
            weights, assets = p.OptimizeSemiDef(method="mean-variance",cardinality=k)
            try:
                pass
            except:
                pass
            ma[j] = p.total_time
            re[j], _ = p.GetReturns()
            ov[j] = p.obj_value
            vv[j] = p.PortfolioVariance()
        #
        k_[i] = p.CheckCardinality(weights)
        mean_time[i] = np.mean(ma)
        std_time[i] =  np.std(ma)
        mean_returns[i] = np.mean(re)
        std_returns[i] = np.std(re)
        m_obj[i] = np.mean(ov)
        s_obj[i] = np.std(ov)
        mean_var[i] = np.mean(vv)
        std_var[i] = np.std(vv)
        i += 1
        
    outfile = "data/0021.npz"
    np.savez(
        outfile,
        K_vec = K_vec,
        k_ = k_,
        mean_time = mean_time,
        mean_returns = mean_returns,
        std_returns = std_returns,
        std_time = std_time,
        m_obj = m_obj,
        s_obj = s_obj,
        mean_var = mean_var
    )

if __name__ == "__main__":
    main()