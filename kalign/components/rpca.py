# rpca.py --- 
# 
# Filename: rpca.py
# Description: 
# Author: Jonathan Chung
# Maintainer: 
# Created: Sun Mar  8 10:00:23 2015 (-0400)
# Version: 
# Package-Requires: ()

# Code:
from component import Kcomponent
import math
import numpy as np
from utils.pyNumpyViewer import pyNumpyViewer

class Rpca(Kcomponent):
    '''
    docs
    '''
    def __init__(self, mu_fac=1.25e7, rho=1.5, lamb=0.05, tol=1e-7, max_iter=1000):
        self.mu_fac = mu_fac
        self.rho = rho
        self.lamb = lamb
        self.tol = tol
        self.max_iter = max_iter
        self.curr_iter = 0
    
    def component(self, kdata):
        '''
        Decompose a matrix into low rank and sparse components.
        Computes the RPCA decomposition using Alternating Lagrangian Multipliers.
        Returns L,S the low rank and sparse components respectively
        '''
        self.curr_iter = 0
        X = np.absolute(kdata["stft"])
        A_hat = np.zeros(X.shape)
        E_hat = np.zeros(X.shape)
        Z = X - A_hat - E_hat

        Y = X
        norm_two = self.L1Norm(Y)
        norm_inf = np.linalg.norm(Y) / self.lamb
        dual_norm = max(norm_two, norm_inf)
        Y = Y / dual_norm
        
        mu = self.mu_fac / norm_two
        x_norm = np.linalg.norm(Y, 'fro') 
        sv = 10
  
        while not self.converged(Z, x_norm):
            temp_T = X - A_hat + (1/mu) * Y
            E_hat = np.maximum(temp_T - self.lamb/mu, 0)
            E_hat += np.minimum(temp_T + self.lamb/mu, 0)

            A_hat = self.svd_shrink(X - E_hat + (mu**-1) * Y, sv, mu)

            Z = X - A_hat - E_hat
            Y = Y + mu * Z
    
        kdata["rpca_l"] = E_hat
        kdata["rpca_s"] = A_hat

    def svd_shrink(self, X, sv, mu):
        """
        Apply the shrinkage operator to the singular values obtained from the SVD of X.
        The parameter tau is used as the scaling parameter to the shrink function.
        Returns the matrix obtained by computing U * shrink(s) * V where 
        U are the left singular vectors of X
        V are the right singular vectors of X
        s are the singular values as a diagonal matrix
        """
        U, S, V = np.linalg.svd(X, sv)   
        svp = S[S>(mu**-1)].shape[0]
        n = X.shape[1]
        if svp < sv:
            sv = min(svp + 1, n)
        else:
            sv = min(svp + np.rint(0.05 * n), n)   
        return U[:, 0:svp] * (S[0:svp] - (mu**-1)) * V[:, 0:svp].T

    @staticmethod
    def shrink(X, tau):
        """
        Apply the shrinkage operator the the elements of X.
        Returns V such that V[i,j] = max(abs(X[i,j]) - tau,0).
        """
        V = np.copy(X).reshape(X.size)
        for i in xrange(V.size):
            V[i] = math.copysign(max(abs(V[i]) - tau, 0), V[i])
            if V[i] == -0:
                V[i] = 0
        return V.reshape(X.shape)

    @staticmethod
    def L1Norm(X):
        """
        Evaluate the L1 norm of X
        Returns the max over the sum of each column of X
        """
        return max(np.sum(X,axis=0))

    def converged(self, Z, d_norm):
        """
        A simple test of convergence based on accuracy of matrix reconstruction
        from sparse and low rank parts
        """
        error = np.linalg.norm(Z, 'fro') / d_norm
        print "error =", error
        if self.curr_iter > self.max_iter:
            return True
        else:
            return error <= self.tol
# rpca.py ends here
