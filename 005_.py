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
# k=5
risk_pref = 0.05
l2_norm_bound = 0.8
ns = 50

cap_init = 1_000_000 # initial capital

dol_per_trade = 1_000_000 # dollars/trade
bal = cap_init # keep track of our account balance
incre =  1 # 1 week = 5 days
old_weights = None
i = 0 # loop counter
loop_range = np.arange(0,len(df23),incre)
trades = np.zeros_like(loop_range)
# years we want to trade
years = 1
for day in loop_range:
    df = pd.read_csv("resources/out_2010_2023.csv",parse_dates=True,index_col="Date") # get our returns estimates, avoiding lookahead bias
    df_ = df.iloc[:-(250*years+2*incre)+day,:ns] # all columns, all rows except the last 250 + week
    df_ = df_.dropna(axis=1,how='any')
    
    # get prices for current week
    prices_current = df_.iloc[-(250*years)+day,:] # prices for the current rebalance period
    shares_per_dollar  = 1/prices_current # how many shares that can be bought with $1
    
    if old_weights is not None: # Liquidate our portfolio from last month and compute return
        # make (or lose) money from selling stocks
        shares_to_sell = (shares_per_dollar * old_weights * dol_per_trade)
        make = np.dot(old_shares_to_own,prices_current)
        # print("Sell and receive: $", make)
        # we get money by selling our old shares at today's prices
        bal = np.round(bal + make,decimals=5)
    else: 
        make = cap_init
    
    # initialize portfolio optimizer
    current_portfolio = Portfolio(stock_prices=df_)
    # Optimize via semidefinite programming
    current_weights, current_assets = current_portfolio.OptimizeSemiDef(
        method = "mean-variance",
        cardinality = k,
        risk_pref = risk_pref,
        l2_norm = l2_norm_bound,) 
    
    # Purchase or short stocks using the weights we find at the prices
    shares_to_own = (shares_per_dollar * current_weights * dol_per_trade) # (s/dollar) * (dollar/dollar) * dollar = shares

    if i < len(loop_range)-1: # don't pay on the last iteration
        pay = np.dot(shares_to_own,prices_current) # how much we pay for owning those 
        
        old_weights = current_weights # Make this week's portfolio be the old portfolio for next week
        old_shares_to_own = shares_to_own # Make this week's portfolio be the old portfolio for next week
        
        trades[i] = np.round(make - pay,decimals=5)
        print(trades[i])
    else:
        print("Not buying on this round")
    
    i +=1 # increase loop counter

sharpe = np.mean(trades) / np.var(trades)
num_up = np.sum(trades > 0)
num_down = np.sum(trades < 0)
updownratio = num_up/num_down

# save the data
outfile = "data/005.npz"
np.savez(
    outfile,
    trades = trades,
    bal = bal,
    sharpe = sharpe,
    updownratio = updownratio
)

