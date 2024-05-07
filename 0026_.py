import numpy as np
from tqdm import tqdm
import pandas as pd
from portfolio import Portfolio
from constants import *

"""
This is script is for evaluating the effector of risk preference
on the semidefinite optimization.
0026ExpRiskPref.py
"""

i = 0
mean_time, std_time = np.zeros((len(risk_pref_vec),)), np.zeros((len(risk_pref_vec),))
mean_returns, std_returns = np.zeros_like(mean_time), np.zeros_like(mean_time)
m_obj, s_obj = np.zeros_like(mean_time), np.zeros_like(mean_time)
mean_var, std_var = np.zeros_like(mean_time), np.zeros_like(mean_time)
k_ = np.zeros_like(mean_time)
#
for risk_pref in tqdm(risk_pref_vec):
    df_ = pd.read_csv("resources/out.csv", parse_dates=True, index_col="Date")
    df_ = df_.dropna(axis=1,how='any')
    df = df_.iloc[:,: ns]
    #
    ma,re= np.zeros((num_trials,)),np.zeros((num_trials,))
    ov, vv= np.zeros_like(re), np.zeros_like(re)
    #
    for j in range(num_trials):
        p = Portfolio(stock_prices = df)
        weights, assets = p.OptimizeSemiDef(
            method="mean-variance",
            cardinality = k,
            risk_pref = risk_pref
            )
        ma[j] = p.total_time
        re[j], _ = p.GetReturns(weights)
        ov[j] = p.obj_value
        vv[j] = p.PortfolioVariance()
    #
    k_[i] = p.CheckCardinality(weights)
    mean_time[i], std_time[i] = np.mean(ma), np.std(ma)
    mean_returns[i], std_returns[i]  = np.mean(re), np.std(re)
    m_obj[i],s_obj[i] = np.mean(ov), np.std(ov)
    mean_var[i], std_var[i] = np.mean(vv), np.std(vv)
    i=i+1
    
outfile = "data/riskpref.npz"
np.savez(
    outfile,
    mean_returns = mean_returns,
    mean_var = mean_var,
    num_stocks = num_stocks,
    std_time = std_time,
    m_obj = m_obj
)