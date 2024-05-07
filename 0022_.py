import numpy as np
import pandas as pd
from portfolio import Portfolio
import matplotlib.pyplot as plt
from heapq import nlargest
from tqdm import tqdm
from constants import *

"""
In this script, we are testing how the total number
of stocks to choose from affects.
0022ExpComputeTime.py
"""

var = num_stocks
mean_time, std_time = np.zeros((len(var),)), np.zeros((len(var),))
mean_returns, std_returns = np.zeros_like(mean_time), np.zeros_like(mean_time)
m_obj, s_obj = np.zeros_like(mean_time), np.zeros_like(mean_time)
mean_var, std_var = np.zeros_like(mean_time), np.zeros_like(mean_time)
i = 0
for ns in tqdm(var):
    df = df_.iloc[:,: ns]
    ma = np.zeros((num_trials,))
    re = np.zeros((num_trials,))
    ov = np.zeros_like(re)
    vv = np.zeros_like(re)
    for j in range(num_trials):
        p = Portfolio(stock_prices = df)
        weights, assets = p.OptimizeSemiDef(method="mean-variance",cardinality=k)
        ma[j] = p.total_time
        re[j], _ = p.GetReturns()
        ov[j] = p.obj_value
        vv[j] = p.PortfolioVariance()
    mean_time[i], std_time[i] = np.mean(ma), np.std(ma)
    mean_returns[i], std_returns[i]  = np.mean(re), np.std(re)
    mean_var[i], std_var[i] = np.mean(vv), np.std(vv)
    m_obj[i] = np.mean(ov)
    s_obj[i] = np.std(ov)
    i+=1 

mean_time, std_time = mean_time.reshape((len(num_stocks),)), std_time.reshape((len(num_stocks),)) 
outfile = "data/computationtime.npz"
np.savez(
    outfile,
    mean_time = mean_time,
    num_stocks = num_stocks,
    mean_returns = mean_returns,
    std_time = std_time,
    mean_var = mean_var,
    m_obj = m_obj,
)