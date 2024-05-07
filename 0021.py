import numpy as np
import matplotlib.pyplot as plt
from constants import *
from matplotlib import rcParams as rcp

rcp['font.family'],rcp['font.serif'] = 'serif', ['Computer Modern Roman']
rcp['text.usetex'] = True
rcp['font.size'], rcp['axes.labelsize'],rcp['axes.titlesize'] = 16, 16,18
rcp['xtick.labelsize'],rcp['ytick.labelsize'] = 14, 14

outfile = "data/cardinality.npz"
npzfile = np.load(outfile)
K_vec = npzfile["K_vec"]
m_obj = npzfile["m_obj"]
mean_returns = npzfile["mean_returns"]
mean_var = npzfile["mean_var"]
k_ = npzfile["k_"]

fig, ax = plt.subplots(2,2, figsize=(10,5))

ax[0,0].plot(K_vec,m_obj,label="Obj. Value",marker="o") # objective function value
ax[0,0].set_xlabel("Cardinality Limit")
ax[0,0].set_ylabel("Obj. Value")
#
ax[1,0].plot(K_vec,mean_returns,label="Returns",marker="o")
ax[1,0].set_xlabel("Cardinality Limit")
ax[1,0].set_ylabel("Portfolio Return")
#
ax[0,1].plot(K_vec, mean_var,label="Variance",marker="o")
ax[0,1].set_xlabel("Cardinality Limit")
ax[0,1].set_ylabel("Portfolio Variance")
#
ax[1,1].plot(K_vec,k_,marker="o")
ax[1,1].set_xlabel("Cardinality Limit")
ax[1,1].set_ylabel("Actual Cardinality")

plt.subplots_adjust(wspace=0.25, hspace=0.8)
fig.savefig('img/0021a.pdf', bbox_inches='tight')

################ Efficient Frontier-like plot
from matplotlib.cm import ScalarMappable
import pylab as pl
#
fig, ax = plt.subplots(1,1,figsize=(7,2))
colors = pl.cm.hsv(K_vec/max(K_vec))
sc = ax.scatter(mean_var, mean_returns, marker='o', c=colors)
#
sm = ScalarMappable(cmap=pl.cm.hsv, norm=plt.Normalize(vmin=min(K_vec), vmax=max(K_vec)))
plt.colorbar(sm, ax=ax,label="Card. Limit")
ax.set_xlabel("Portfolio Variance")
ax.set_ylabel("Portfolio Return")
plt.subplots_adjust(wspace=0.3, hspace=0.7)
#
fig.savefig("img/0021b.pdf",bbox_inches="tight")
