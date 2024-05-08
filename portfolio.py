import numpy as np
import cvxpy as cp
import pandas as pd
import mosek.fusion as mf
from pypfopt import risk_models
from pypfopt import expected_returns
import sys
import os
import time

def low_rank_approx(A=None, r=1):
    u,s,v = np.linalg.svd(A, full_matrices=False)
    Ar = np.zeros((len(u), len(v)))
    for i in range(r):
        Ar += s[i] * np.outer(u.T[i], v[i])
    return Ar

class Portfolio():
    def __init__(self, mu=None, sigma=None, stock_prices: pd.DataFrame=None):
        
        self.stock_prices = stock_prices
        if stock_prices is not None:
            self.stock_prices = self.stock_prices.dropna(axis=1,how='any')
            self.mu = (expected_returns.mean_historical_return(self.stock_prices, frequency=252)).to_numpy()
            S = risk_models.semicovariance(self.stock_prices, returns_data=False, frequency=252)
            S = risk_models.fix_nonpositive_semidefinite(S, fix_method="spectral")
            self.sigma = S.to_numpy()
        else:
            self.mu = mu
            self.sigma = sigma
            self.stock_prices = 0

        self.n = len(self.mu)
        self.risk_pref = 0.01
        self.obj_value = None
        self.w_opt = None
        self.T = self.stock_prices.shape[0] # sample size
        return None
    
    def OptimizeCVX(
        self, 
        method: str = "mean-variance", # or "robust"
        long_only = True, # is this a long-only portfolio?
        l2_norm: float = None,
        risk_pref: float = 0.01,
        T = None # sample size
        ):
        self.T = T if T is not None else self.T
        self.risk_pref = risk_pref
        sigma_mu = 1/self.T * np.diag(np.diag(self.sigma))
        epsil = 500 * sigma_mu # set arbitrary for now
        mu_hat = self.mu # set equal to mu_hat for now
        self.w = cp.Variable((self.n,1),nonneg=True) if long_only else cp.Variable((self.n,1)) 

        constraints = [np.ones((self.n,1)).T @ self.w == 1.,]     # constrain elements of w to sum to 1
        
        obj_arg = cp.quad_form(self.w,self.sigma)
        if method == "mean-variance":
            obj_arg +=  - self.risk_pref * self.mu.T @ self.w
        elif method == "robust":
            gamma = 0.05
            obj_arg += - self.risk_pref * \
                (mu_hat.T @ self.w - gamma*cp.sqrt(cp.quad_form(self.w,sigma_mu)))
            
        if l2_norm is not None:
            constraints.append(cp.norm(self.w,2) <= l2_norm)
        
        objective = cp.Minimize(obj_arg)
        t0 = time.time()
        prob = cp.Problem(objective, constraints)
        self.obj_value = prob.solve(solver=cp.MOSEK,verbose=False)
        t1 = time.time()
        self.w_opt = self.w.value.reshape(self.n,)
        self.weights = self.w_opt
        self.mu_portfolio = np.dot(self.w_opt,self.mu)
        assets = self.stock_prices.columns   
        self.total_time = t1 - t0 
        return self.weights, assets
    
    def OptimizeSemiDef(
        self,
        method: str      = "mean-variance",
        cardinality      = 5, # no constraint
        l2_norm: float   = None,
        risk_pref: float = 0.01,
        epsil = None
        ):
        n_ = self.n
        stock_prices_ = self.stock_prices
        self.stock_prices_ = stock_prices_
        mu_ = (expected_returns.ema_historical_return(stock_prices_, frequency=252, span=500)).to_numpy()
        sigma_ = risk_models.semicovariance(stock_prices_, returns_data=False, frequency=252)
        sigma_ = risk_models.fix_nonpositive_semidefinite(sigma_, fix_method="spectral")
        sigma_ = sigma_.to_numpy()
        self.sigma_, self.sigma = sigma_, sigma_
        self.mu_, self.mu = mu_, mu_
        iota = np.ones((n_,1))
        self.iota = iota
        Iota = np.ones((n_,n_))
        W = cp.Variable((n_,n_), PSD = True)
        k = cardinality
        objective = cp.Minimize(cp.trace(sigma_ @ W) - risk_pref * (iota.T @ W @ mu_))
        #
        constraints = [
            cp.trace(Iota @ W) == 1,
            cp.quad_form(iota, cp.abs(W)) <= k * cp.trace(W),
        ]
        
        # Adding the constraint on the L2 norm bound
        if l2_norm is not None:
            constraints.append(cp.trace(W) <= l2_norm**2)
            
        self.S_mu = 1/self.T * np.diag(np.diag(self.sigma))
        # Adding the robustness constraint
        if epsil is not None:
            constraints.append(cp.trace(self.S_mu @ W) <= epsil)
            
        t0 = time.time() # timing the optimization solver
        prob = cp.Problem(objective, constraints)
        self.obj_value = prob.solve(solver=cp.MOSEK,verbose=False)
        t1 = time.time()
        self.total_time = t1 - t0
        self.W_opt = low_rank_approx(W.value)
        self.weights = np.sqrt(np.diag(self.W_opt)) * np.sign(self.mu)
        assets = self.stock_prices.columns
        return self.weights, assets
    
    def CheckCardinality(self,weights=None,tol=1e-5):
        weights = weights if weights is not None else self.weights
        return sum(weights > tol)
    
    def EnforceCardinality(self,weights,k):
        x = weights
        w_n = np.zeros((k,))
        for i in range(k):
            idx = np.argmax((x))
            x = np.delete(x, [idx])
            w_n[i] = np.max(x)
        weights = np.where(weights > min(w_n), weights, 0)
        weights = weights / np.sum(weights) # scale
        self.weights = weights
        return self.weights
    
    def CheckWeights(self,weights=None,tol=1e-5):            
        w_ = weights if weights is not None else self.weights
        s_ = np.sum(w_)
        if np.sum(np.abs(s_ - 1)) <  tol:
            print(f"Weight allocation sums to {np.round(s_,4)}")
        return None
    
    def GetReturns(self,weights=None):
        weights = weights if weights is not None else self.weights
        return np.dot(weights, self.mu ), weights * self.mu
    
    def PortfolioVariance(self,w = None, sigma=None):
        w = self.weights if w is None else w
        sigma = self.sigma if sigma is None else sigma
        return w.T @ sigma @ w