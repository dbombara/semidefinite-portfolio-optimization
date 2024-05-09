import numpy as np
import pandas as pd

## Parameters for Experiments
k = 5 # cardinality
ns = 70 # number of stocks under consideration
num_trials = 2
risk_pref = 0.01

# cardinality_EF = np.arange(5,ns,5)

## Variables
K_vec = np.arange(2,50+1) # cardinalities to test
num_stocks = np.arange(10,100) # number of stocks to test
risk_pref_vec = np.arange(0.01, 1, 0.01)
deltavec = np.arange(0.5,1.25,0.01)

df_ = pd.read_csv("resources/out.csv", parse_dates=True, index_col="Date")
df_ = df_.dropna(axis=1,how='any') # also return the indices of the columns that were dropped