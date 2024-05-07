import numpy as np
from tqdm import tqdm
import pandas as pd
from portfolio import Portfolio
from constants import *

"""_summary_
0023ExpEfficientFrontier.py
"""

i = 0
k_ = np.zeros_like(risk_pref_vec)
k__ = np.zeros_like(risk_pref_vec)

returns = np.zeros_like(k_)
returns_k = np.zeros_like(k_)
variance = np.zeros_like(k_)
variance_k = np.zeros_like(k_)

for risk_pref in tqdm(risk_pref_vec):
    df = df_.iloc[:,: ns]
    p = Portfolio(stock_prices = df)
    weights, assets = p.OptimizeSemiDef(
        method="mean-variance",
        cardinality = k,
        risk_pref = risk_pref
        )
    try:
        weights_k = p.EnforceCardinality(weights,k)
    except:
        weights_k = weights
    
    k_[i] = p.CheckCardinality(weights)
    k__[i] = p.CheckCardinality(weights_k)
    #
    returns[i], _ = p.GetReturns(weights)
    returns_k[i], _= p.GetReturns(weights_k)
    #
    variance[i] = p.PortfolioVariance(weights)
    variance_k[i] = p.PortfolioVariance(weights_k)
    #
    i += 1
    
outfile = "data/efficientfrontier.npz"
np.savez(
    outfile,
    k_ = k_,
    k__ = k__,
    returns = returns,
    returns_k = returns_k,
    weights = weights,
    weights_k = weights_k,
    variance = variance,
    variance_k = variance_k
)
    
    
    