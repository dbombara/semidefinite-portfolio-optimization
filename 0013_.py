import numpy as np
from tqdm import tqdm
import pandas as pd
from portfolio import Portfolio
from constants import *

"""0013.py
previously: EfficientFrontierNumStocks.py
"""

i, j = 0 ,0
n1 = len(num_stocks)
n2 = len(risk_pref_vec)

returns = np.zeros((n1,n2))
variance = np.zeros_like(returns)
obj_val = np.zeros_like(variance)

for risk_pref in tqdm(risk_pref_vec):
    i = 0
    for ns in tqdm(num_stocks):
        df = df_.iloc[:,: ns]
        p = Portfolio(stock_prices = df)
        weights, assets = p.OptimizeSemiDef(
            method="mean-variance",
            cardinality = k,
            risk_pref = risk_pref
            )
        returns[i,j], _ = p.GetReturns(weights)
        variance[i,j] = p.PortfolioVariance(weights)
        obj_val[i,j] = p.obj_value
        i += 1
    j += 1
    
#outfile = "data/EfficientFrontierNumStocks.npz"
outfile = "data/0013.npz"
np.savez(
    outfile,
    num_stocks = num_stocks,
    risk_pref_vec = risk_pref_vec,
    returns = returns,
    variance = variance,
    obj_val = obj_val,
)