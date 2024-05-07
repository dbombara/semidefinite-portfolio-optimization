import numpy as np
from tqdm import tqdm
import pandas as pd
from constants import *
from portfolio import Portfolio

# 0024ExpL2Bounds.py

i = 0
var = deltavec

returns, variance, obj_val_ = np.zeros_like(var), np.zeros_like(var), np.zeros_like(var)

for delta in tqdm(deltavec):
    df = df_.iloc[:,:ns]
    p = Portfolio(stock_prices = df)
    weights, assets = p.OptimizeSemiDef(
        method="mean-variance",
        cardinality = k,
        l2_norm=delta
        )
    returns[i], _ = p.GetReturns(weights)
    variance[i] = p.PortfolioVariance(weights)
    obj_val_[i] = p.obj_value
    i+=1
    
outfile = "data/l2norm.npz"

np.savez(
    outfile,
    returns=returns,
    variance=variance,
    deltavec=deltavec,
    obj_val = obj_val_
)

