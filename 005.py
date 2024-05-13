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
risk_pref = 0.5
l2_norm_bound = 0.8
ns = 70
# p = Portfolio(stock_prices = df)
# weights, assets = p.OptimizeSemiDef(
#     method = "mean-variance",
#     cardinality = k,
#     risk_pref = risk_pref,
#     l2_norm = 0.78,
# )

#df2023_ =df23[assets]
# start_prices  = (df2023_.iloc[0,:])
# end_prices = (df2023_.iloc[-1,:])
# annual2023return = (end_prices - start_prices)/start_prices
# print(np.dot(annual2023return,weights))

# print(len(df23)) # 250 trading days per year

cap_init = 1_000_000 # initial capital

dol_per_trade = 1_000_000 # dollars/trade
bal = cap_init # keep track of our account balance
incre = 20 # increments of 20 days (four weeks)
old_weights = None
i = 0 # loop counter
for day in range(0,len(df23),incre):
    df = pd.read_csv("resources/out_2010_2023.csv",parse_dates=True,index_col="Date") # get our returns estimates, avoiding lookahead bias
    df_ = df.iloc[:-255+day,:ns] # all columns, all rows except the last 250 + week
    df_ = df_.dropna(axis=1,how='any')
    
    
    # get prices for current week
    prices_current = df_.iloc[-250+day,:] # prices for the current rebalance period
    shares_per_dollar  = 1/prices_current # how many shares that can be bought with $1
    
    if old_weights is not None:
        # # make (or lose) money from selling stocks
        # prices_last_rebalance = df_.iloc[-250+day-incre,:] # prices at the last rebalancing period
        
        # # Liquidate our portfolio from last month and compute return
        # shares_per_dollar_last_rebalance = 1/prices_last_rebalance
        shares_to_sell = shares_per_dollar * old_weights * dol_per_trade
        make = np.dot(old_shares_to_own,prices_current)
        # print("Sell and receive: $", make)
        # we get money by selling our old shares at today's prices
        bal = bal + make
    
    # initilaze portfolio optimizer
    current_portfolio = Portfolio(stock_prices=df_)
    # Optimize via semidefinite programming
    current_weights, current_assets = current_portfolio.OptimizeSemiDef(
        method = "mean-variance",
        cardinality = k,
        risk_pref = risk_pref,
        l2_norm = l2_norm_bound,) 
    
    # Purchase or short stocks using the weights we find at the prices
    
    shares_to_own = shares_per_dollar * current_weights * dol_per_trade # (s/dollar) * (dollar/dollar) * dollar = shares

    # how much we pay for owning those 
    pay = np.dot(shares_to_own,prices_current)
    # print("Buy and pay: $",pay)

    # our current balance
    bal = bal - pay
    
    # Make this week's portfolio be the old portfolio for next week
    old_weights = current_weights
    old_shares_to_own = shares_to_own
    
    # buysell = np.dot(weights,)
    # print(buysell)
    print((bal - cap_init)/cap_init*100)
    i +=1
    # if i == 4:
    #     break
    


    



