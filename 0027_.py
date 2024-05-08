import numpy as np
import pandas as pd
from portfolio import Portfolio
import matplotlib.pyplot as plt
from heapq import nlargest
from tqdm import tqdm
from constants import *

"""_summary_
In this script, we explore robust optimization
"""

i = 0
epsil_vec = np.arange(2e-6,10e-6,0.1e-6)
k = 5
var = epsil_vec

returns, variance, obj_val_ = np.zeros_like(var), np.zeros_like(var), np.zeros_like(var)

for epsil in tqdm(var):
    df = df_.iloc[:,:ns]
    p = Portfolio(stock_prices = df)
    weights, assets = p.OptimizeSemiDef(
        method="mean-variance",
        cardinality = k,
        risk_pref=0.01,
        l2_norm=None,
        epsil=epsil,
        )
    returns[i], _ = p.GetReturns(weights)
    variance[i] = p.PortfolioVariance(weights)
    obj_val_[i] = p.obj_value
    i+=1
outfile = "data/0027.npz"

np.savez(
    outfile,
    returns=returns,
    variance=variance,
    epsil_vec = epsil_vec,
    obj_val = obj_val_
)

