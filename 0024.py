import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from constants import *
from matplotlib import rcParams as rcp
from matplotlib.cm import ScalarMappable

rcp['font.family'],rcp['font.serif'] = 'serif', ['Computer Modern Roman']
rcp['text.usetex'] = True
rcp['font.size'], rcp['axes.labelsize'],rcp['axes.titlesize'] = 16, 16,18
rcp['xtick.labelsize'],rcp['ytick.labelsize'] = 14, 14

nf = np.load("data/l2norm.npz")
returns, variance, deltavec, obj_val = nf["returns"],  nf["variance"], nf["deltavec"], nf["obj_val"]

###### Plot 1 #################################################
fig, ax = plt.subplots(1,1,figsize=(7,2))
colors = pl.cm.hsv(deltavec)
sc = ax.scatter(variance, returns, marker="o",c=colors)
sm = ScalarMappable(cmap=pl.cm.hsv, norm=plt.Normalize(vmin=min(deltavec), vmax=max(deltavec)))
plt.colorbar(sm, ax=ax, label="$L_2$-Norm Constraint")
ax.set_xlabel("Portfolio Variance"), ax.set_ylabel("Portfolio Return")
plt.subplots_adjust(wspace=0.3, hspace=0.7)
fig.savefig("img/00241.pdf",bbox_inches="tight")

###### Plot 2: Plot direct correlations #################################################
fig, ax = plt.subplots(1,3,figsize=(9,4))
ax[0].plot(deltavec, returns)
ax[0].set_ylabel("Portfolio Returns")
ax[0].set_xlabel("$L_2$-Norm Bound, $\delta$")
#
ax[1].plot(deltavec, variance)
ax[1].set_xlabel("$L_2$-Norm Bound, $\delta$")
ax[1].set_ylabel("Portfolio Variance")
#
ax[2].plot(deltavec, obj_val)
ax[2].set_xlabel("$L_2$-Norm Bound, $\delta$")
ax[2].set_ylabel("Objective Value")
#
plt.subplots_adjust(wspace=0.7, hspace=0.7)
fig.savefig("img/00242.pdf",bbox_inches="tight")