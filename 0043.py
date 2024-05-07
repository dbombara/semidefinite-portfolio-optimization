import numpy as np
from constants import *
from portfolio import Portfolio
import matplotlib.pyplot as plt

from pypfopt import risk_models

from matplotlib import rcParams as rcp
rcp['font.family'],rcp['font.serif'] = 'serif', ['Computer Modern Roman']
rcp['text.usetex'] = True
rcp['font.size'], rcp['axes.labelsize'],rcp['axes.titlesize'] = 16, 16,18
rcp['xtick.labelsize'],rcp['ytick.labelsize'] = 14, 14

df = df_.iloc[:,:10]
p = Portfolio(stock_prices = df)

import seaborn as sns
fig, ax = plt.subplots(2,1,figsize=(8,4))
sns.heatmap((p.sigma), annot=False,linewidths=0.5,ax=ax[0])
ax[0].set_title("Sample Covariance Matrix")
ax[0].set_xlabel("Stock Index")
ax[0].set_ylabel("Stock Index")

sns.heatmap(risk_models.cov_to_corr(p.sigma), annot=False,linewidths=0.5,ax=ax[1])
ax[1].set_title("Sample Correlation Matrix")
ax[1].set_xlabel("Stock Index")
ax[1].set_ylabel("Stock Index")

plt.subplots_adjust(wspace=0.3, hspace=0.8)
fig.savefig('img/0043.pdf', bbox_inches='tight')