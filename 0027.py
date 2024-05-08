import numpy as np
import matplotlib.pyplot as plt
from constants import *

## Parameters for Plotting
from matplotlib import rcParams as rcp
rcp['font.family'],rcp['font.serif'] = 'serif', ['Computer Modern Roman']
rcp['text.usetex'] = True
rcp['font.size'], rcp['axes.labelsize'],rcp['axes.titlesize'] = 16, 16,18
rcp['xtick.labelsize'],rcp['ytick.labelsize'] = 14, 14

nf = np.load("data/0027.npz")
returns = nf["returns"]
variance = nf["variance"]
epsil_vec = nf["epsil_vec"]
obj_val = nf["obj_val"]

fig, ax = plt.subplots(1,3, figsize=(10,5))
#
ax[0].plot(epsil_vec,returns,label="Obj. Value",marker="o") # objective function value
ax[0].set_xlabel("$\epsilon$")
ax[0].set_ylabel("Obj. Value")
#
ax[1].plot(epsil_vec,variance,label="Returns",marker="o")
ax[1].set_xlabel("$\epsilon$")
ax[1].set_ylabel("Expected Portfolio Return")
ax[1].set_title("Robust Optimizaton")
#
ax[2].plot(epsil_vec, obj_val,label="Variance",marker="o")
ax[2].set_xlabel("$\epsilon$")
ax[2].set_ylabel("Portfolio Variance")
#
plt.subplots_adjust(wspace=0.5, hspace=0.7)
fig.savefig('img/0027a.pdf', bbox_inches='tight')


# Efficient Frontier
# epsil_vec = epsil_vec[:60]
# returns = returns[:60]
# variance = variance[:60]

import pylab as pl
from matplotlib.cm import ScalarMappable
fig, ax = plt.subplots(1,1,figsize=(7,2))
colors = pl.cm.hsv(epsil_vec/max(epsil_vec))
sc = ax.scatter(variance, returns, marker="o",c=colors)
sm = ScalarMappable(cmap=pl.cm.hsv, norm=plt.Normalize(vmin=min(epsil_vec), vmax=max(epsil_vec)))
plt.colorbar(sm, ax=ax, label="$\epsilon$")
ax.set_xlabel("Portfolio Variance"), ax.set_ylabel("Portfolio Return")
plt.subplots_adjust(wspace=0.3, hspace=0.7)
fig.savefig("img/0027b.pdf",bbox_inches="tight")
plt.show()