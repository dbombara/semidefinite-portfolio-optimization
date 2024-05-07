import numpy as np
import pandas as pd
from portfolio import Portfolio
from constants import *
# Read in price data
# 0025ExpReturnsMV.py

df = df_.iloc[:,:ns]
p = Portfolio(stock_prices = df)
weights, assets = p.OptimizeSemiDef(method="mean-variance",cardinality=k)
t_ = p.total_time
totalReturns, returns = p.GetReturns()
cw = p.CheckWeights(weights)
weights_ = p.EnforceCardinality(weights,k)

outfile = "data/returnsMV.npz"
np.savez(
    outfile,
    weights_  = weights_,
    weights = weights,
)
