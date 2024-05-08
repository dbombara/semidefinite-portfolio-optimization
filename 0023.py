import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from constants import *
from matplotlib import rcParams as rcp

"""The efficient frontier shows the tradeoff between 
    expected returns and portfolio variance for different levels of lambda
"""

# set plottting parameters
rcp['font.family'],rcp['font.serif'] = 'serif', ['Computer Modern Roman']
rcp['text.usetex'] = True
rcp['font.size'], rcp['axes.labelsize'],rcp['axes.titlesize'] = 16, 16,18
rcp['xtick.labelsize'],rcp['ytick.labelsize'] = 14, 14

# Load data
nf = np.load("data/efficientfrontier.npz")
k_, k__ = nf["k_"], nf["k__"]
returns, returns_k = nf["returns"], nf["returns_k"]
weights, weights_k = nf["weights"], nf["weights_k"]
variance, variance_k = nf["variance"], nf["variance_k"]

from matplotlib.cm import ScalarMappable

fig, ax = plt.subplots(1,1,figsize=(7,2))
colors = pl.cm.hsv(risk_pref_vec/max(risk_pref_vec))
sc = ax.scatter(variance, returns, marker='o', c=colors)

sm = ScalarMappable(cmap=pl.cm.hsv, norm=plt.Normalize(vmin=min(risk_pref_vec), vmax=max(risk_pref_vec)))
plt.colorbar(sm, ax=ax,label="Risk Preference")
#
ax.set_xlabel("Portfolio Variance")
ax.set_ylabel("Portfolio Return")
ax.set_title("Efficient Frontier")
plt.subplots_adjust(wspace=0.3, hspace=0.7)
fig.savefig("img/0023.pdf",bbox_inches="tight")

######## Plot Sharpe Ratio next
sr = returns/np.sqrt(variance)

fig, ax = plt.subplots(1,1,figsize=(7,2))
colors = pl.cm.hsv(returns/max(returns))
sc = ax.scatter(risk_pref_vec, sr, marker='o', c=colors)

sm = ScalarMappable(cmap=pl.cm.hsv, norm=plt.Normalize(vmin=min(returns), vmax=max(returns)))
plt.colorbar(sm, ax=ax,label="Expected Return")

ax.set_title("Sharpe Ratio $S$ for Varying $\lambda$")
ax.set_xlabel("Risk, $\lambda$")
ax.set_ylabel("Sharpe Ratio")

plt.subplots_adjust(wspace=0.3, hspace=0.7)
fig.savefig("img/0023b.pdf",bbox_inches="tight")
plt.show()

# sc = ax.scatter(risk_pref_vec, sr, marker='o', c=colors)

# sm = ScalarMappable(cmap=pl.cm.hsv, norm=plt.Normalize(vmin=min(risk_pref_vec), vmax=max(risk_pref_vec)))
# plt.colorbar(sm, ax=ax,label="Risk Preference")
# ax.set_xlabel("Portfolio Variance")
# ax.set_ylabel("Portfolio Return")
# ax.set_title("Efficient Frontier")
# plt.subplots_adjust(wspace=0.3, hspace=0.7)
# fig.savefig("img/0023.pdf",bbox_inches="tight")
