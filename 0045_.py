import numpy as np
from tqdm import tqdm
import pandas as pd
from portfolio import Portfolio
from constants import *

i, j = 0 ,0
risk_pref_vec = np.arange(0.01, 1, 0.05)
epsil_vec = np.arange(2e-6,10e-6,0.5e-6)
n1 = len(epsil_vec)
n2 = len(risk_pref_vec)

returns = np.zeros((n1,n2))
variance = np.zeros_like(returns)
obj_val = np.zeros_like(variance)

for risk_pref in tqdm(risk_pref_vec):
    i = 0
    for epsil in tqdm(epsil_vec):
        df = df_.iloc[:,: ns]
        p = Portfolio(stock_prices = df)
        weights, assets = p.OptimizeSemiDef(
            method="mean-variance",
            cardinality = k,
            risk_pref = risk_pref,
            epsil = epsil
            )

        returns[i,j], _ = p.GetReturns(weights)
        variance[i,j] = p.PortfolioVariance(weights)
        obj_val[i,j] = p.obj_value
        i += 1
    j += 1
    
outfile = "data/0045.npz"
np.savez(
    outfile,
    epsil_vec = epsil_vec,
    risk_pref_vec = risk_pref_vec,
    returns = returns,
    variance = variance,
    obj_val = obj_val,
)