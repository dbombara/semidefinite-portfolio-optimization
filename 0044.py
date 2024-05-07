import numpy as np
from constants import *
from portfolio import Portfolio
import matplotlib.pyplot as plt
from matplotlib import rcParams as rcp

rcp['font.family'],rcp['font.serif'] = 'serif', ['Computer Modern Roman']
rcp['text.usetex'] = True
rcp['font.size'], rcp['axes.labelsize'],rcp['axes.titlesize'] = 16, 16,18
rcp['xtick.labelsize'],rcp['ytick.labelsize'] = 14, 14

df = df_.iloc[:,:]
p = Portfolio(stock_prices = df)
fig, ax1 = plt.subplots(2,1,figsize=(8,4))
markerline, stemline, baseline, = ax1[0].stem(p.mu,linefmt='k-',markerfmt='ro',basefmt='k.')
plt.setp(stemline, linewidth = 1.25)
plt.setp(markerline, markersize = 2)
ax1[0].set_xlabel("Stock Index")
ax1[0].set_ylabel("Expected Return")
ax1[0].set_title("Stocks in the S\&P 500")

df = df_.iloc[:,:ns]
p = Portfolio(stock_prices = df)
markerline, stemline, baseline, = ax1[1].stem(p.mu,linefmt='k-',markerfmt='ro',basefmt='k.')
plt.setp(stemline, linewidth = 1.25)
plt.setp(markerline, markersize = 5)
ax1[1].set_xlabel("Stock Index")
ax1[1].set_ylabel("Expected Return")
ax1[1].set_title("Selected Stocks for Optimization")
plt.subplots_adjust(wspace=0.3, hspace=0.7)
fig.savefig("img/0044.pdf")
