import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from constants import *
from matplotlib import rcParams as rcp
from matplotlib.cm import ScalarMappable
from tqdm import tqdm
from matplotlib import cm
from matplotlib.ticker import LinearLocator

rcp['font.family'],rcp['font.serif'] = 'serif', ['Computer Modern Roman']
rcp['text.usetex'] = True
rcp['font.size'], rcp['axes.labelsize'],rcp['axes.titlesize'] = 16, 16,18
rcp['xtick.labelsize'],rcp['ytick.labelsize'] = 14, 14

nf = np.load("data/EfficientFrontierCardinality.npz")

returns, variance = nf["returns"], nf["variance"]
cardinality_EF, risk_pref_vec, obj_val = nf["cardinality_EF"], nf["risk_pref_vec"], nf["obj_val"]
n1 = len(cardinality_EF)
n2 = len(risk_pref_vec)
fig, ax = plt.subplots(1,1, figsize=(7,2))
colors = pl.cm.hsv(risk_pref_vec/max(risk_pref_vec))

# the cardinality_EF index is along the first dimension obj_val[i,:]

for i in tqdm(range(len(cardinality_EF))):
    returns_ = returns[i,:]
    variance_ = variance[i,:]
    obj_val_ = obj_val[i,:]
    
    ax.plot(variance_, returns_)

#### get meshgrid
riskPrefMat, cardinalityMat = np.meshgrid(risk_pref_vec,cardinality_EF)

###### Plot Returns
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(riskPrefMat,cardinalityMat,returns,cmap=cm.coolwarm,linewidth=0, antialiased=False)
ax.set_title("Returns")
ax.set_xlabel("Risk")
ax.set_ylabel("Carinality")
fig.colorbar(surf, shrink=0.5, aspect=5)
#fig.savefig("img/efficientfrontiercardinality_returns.png")
plt.subplots_adjust(wspace=0.8, hspace=0.7)
fig.savefig("img/png/0011a.png", bbox_inches='tight')
fig.savefig("img/0011a.pdf", bbox_inches='tight')

######## Plot Variance
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(riskPrefMat,cardinalityMat,variance,cmap=cm.coolwarm,linewidth=0, antialiased=False)
ax.set_title("Variance")
ax.set_xlabel("Risk")
ax.set_ylabel("Carinality")
fig.colorbar(surf, shrink=0.5, aspect=5)
#fig.savefig("img/efficientfrontiercardinality_variance.png")
plt.subplots_adjust(wspace=0.8, hspace=0.7)
fig.savefig("img/png/0011b.png", bbox_inches='tight')
fig.savefig("img/0011b.pdf", bbox_inches='tight')

####### Plot obj value
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(riskPrefMat,cardinalityMat,obj_val,cmap=cm.coolwarm,linewidth=0, antialiased=False)
ax.set_title("Objective Value")
ax.set_xlabel("Risk")
ax.set_ylabel("Carinality")
fig.colorbar(surf, shrink=0.5, aspect=5)
# fig.savefig("img/efficientfrontiercardinality_objective.png")
plt.subplots_adjust(wspace=0.8, hspace=0.7)
fig.savefig("img/png/0011c.png", bbox_inches='tight')
fig.savefig("img/0011c.pdf", bbox_inches='tight')

plt.show()