import numpy as np
from tqdm import tqdm
import pandas as pd
from portfolio import Portfolio
from constants import *

"""0012_.py
This script is for generating the efficient frontier for different constraints and the L2 norm and different risk preferences.
"""

i, j = 0 ,0
n1 = len(deltavec)
n2 = len(risk_pref_vec)

returns = np.zeros((n1,n2))
variance = np.zeros_like(returns)
obj_val = np.zeros_like(variance)

for risk_pref in tqdm(risk_pref_vec):
    i = 0
    for l2_norm in tqdm(deltavec):
        df = df_.iloc[:,: ns]
        p = Portfolio(stock_prices = df)
        weights, assets = p.OptimizeSemiDef(
            method="mean-variance",
            cardinality = k,
            risk_pref = risk_pref,
            l2_norm = l2_norm
            )

        returns[i,j], _ = p.GetReturns(weights)
        variance[i,j] = p.PortfolioVariance(weights)
        obj_val[i,j] = p.obj_value
        i += 1
    j += 1
    
outfile = "data/EfficientFrontierL2Norm.npz"
np.savez(
    outfile,
    deltavec = deltavec,
    risk_pref_vec = risk_pref_vec,
    returns = returns,
    variance = variance,
    obj_val = obj_val,
)