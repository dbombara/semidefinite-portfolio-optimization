# Script for matching the 2023 stocks with the optimized stocks from 2010 through 2022
import numpy as np
from tqdm import tqdm
import pandas as pd
from portfolio import Portfolio
from constants import *
from pypfopt.expected_returns import returns_from_prices

"""003.py
Script for matching the 2023 stocks with the optimized stocks from 2010 through 2022
"""
k=5
df = df_.iloc[:,: ns]
p = Portfolio(stock_prices = df)
weights, assets = p.OptimizeSemiDef(
    method = "mean-variance",
    cardinality = k,
    risk_pref = risk_pref,
    l2_norm = 0.78,
)

df2023_ =df23[assets]
mu2023 = returns_from_prices(df2023_, log_returns=False)
start_prices  = (df2023_.iloc[0,:])
end_prices = (df2023_.iloc[-1,:])
annual2023return = (end_prices - start_prices)/start_prices
print(np.dot(annual2023return,weights))

