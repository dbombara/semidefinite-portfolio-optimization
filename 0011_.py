import numpy as np
from tqdm import tqdm
import pandas as pd
from portfolio import Portfolio
from constants import *

"""0011_.py
This script is used to generate the efficient frontier for different cardinality constraints and risk preferences.
"""

i, j = 0 ,0
cardinality_EF = np.arange(5,ns,5)
#risk_pref_vec = np.arange(0.01,0.05,0.01)
n1 = len(cardinality_EF)
n2 = len(risk_pref_vec)

returns = np.zeros((n1,n2))
variance = np.zeros_like(returns)
obj_val = np.zeros_like(variance)

for risk_pref in tqdm(risk_pref_vec):
    i = 0
    for k_EF in tqdm(cardinality_EF):
        df = df_.iloc[:,: ns]
        p = Portfolio(stock_prices = df)
        weights, assets = p.OptimizeSemiDef(
            method="mean-variance",
            cardinality = k_EF,
            risk_pref = risk_pref
            )

        returns[i,j], _ = p.GetReturns(weights)
        variance[i,j] = p.PortfolioVariance(weights)
        obj_val[i,j] = p.obj_value
        i += 1
    j += 1
    
outfile = "data/EfficientFrontierCardinality.npz"
np.savez(
    outfile,
    cardinality_EF = cardinality_EF,
    risk_pref_vec = risk_pref_vec,
    returns = returns,
    variance = variance,
    obj_val = obj_val,
)