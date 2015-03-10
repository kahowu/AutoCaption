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
import irlb
from utils.pyNumpyViewer import pyNumpyViewer

class Rpca(Kcomponent):
    '''
    docs
    '''
    def __init__(self, mu_fac=125, rho=1.5, lamb=0.05, tol=1e-7,
                 max_iter=1000, mask=True, gain=1, debug=False):
        self.mu_fac = mu_fac # tune this
        self.rho = rho # tune this
        self.lamb = lamb
        self.tol = tol
        self.max_iter = max_iter
        self.curr_iter = 0
        self.mask = mask
        self.gain = gain
        self.debug = debug
    
    def component(self, kdata):
        '''
        Decompose a matrix into low rank and sparse components.
        Computes the RPCA decomposition using Alternating Lagrangian Multipliers.
        Returns L,S the low rank and sparse components respectively
        '''
        self.curr_iter = 0
        D = kdata["stft"]
        X = np.absolute(D)
        A_hat = np.zeros(X.shape)
        E_hat = np.zeros(X.shape)
        Z = X - A_hat - E_hat

        Y = X
        norm_two = self.L1Norm(Y)
        norm_inf = np.linalg.norm(Y) / self.lamb
        dual_norm = max(norm_two, norm_inf)
        Y = Y / dual_norm

        mu = self.mu_fac / norm_two
        mu_bar = mu * 1e7
        x_norm = np.linalg.norm(X, 'fro') 
        sv = 10   

        while not self.converged(Z, x_norm):
            temp_T = X - A_hat + (1/mu) * Y
            E_hat = np.maximum(temp_T - self.lamb/mu, 0)
            E_hat += np.minimum(temp_T + self.lamb/mu, 0)

            A_hat = self.svd_shrink(X - E_hat + (mu**-1) * Y, sv, mu)

            Z = X - A_hat - E_hat
            Y = Y + mu * Z
            mu = min(mu * self.rho, mu_bar)

        shift = 1j * self.angle(D)
        E = E_hat * np.exp(shift)
        A = A_hat * np.exp(shift)

        if self.mask:
            m = np.absolute(E) > (self.gain * np.absolute(A))

            E_out = m * D
            A_out = D - E_out
        else:
            E = E_out
            A = A_out

        kdata["rpca_e"] = E_out
        kdata["rpca_a"] = A_out

    def svd_shrink(self, X, sv, mu):
        """
        Apply the shrinkage operator to the singular values obtained from the SVD of X.
        The parameter tau is used as the scaling parameter to the shrink function.
        Returns the matrix obtained by computing U * shrink(s) * V where 
        U are the left singular vectors of X
        V are the right singular vectors of X
        s are the singular values as a diagonal matrix
        """
        svd = irlb.irlb(X, sv, maxit=self.max_iter)
        U = svd[0]
        S = svd[1]
        V = svd[2]
        svp = S[S>(mu**-1)].shape[0]
        n = X.shape[1]
        if svp < sv:
            sv = min(svp + 1, n)
        else:
            sv = min(svp + np.rint(0.05 * n), n)
            
        U_ = U[:, 0:svp]
        S_ = (S[0:svp] - (mu**-1))
        V_ = V[:, 0:svp].T
        output = np.dot((U_ * S_), V_)  

        return output

    @staticmethod
    def L1Norm(X):
        """
        Evaluate the L1 norm of X
        Returns the max over the sum of each column of X
        """
        return max(np.sum(X,axis=0))

    def converged(self, Z, x_norm):
        """
        A simple test of convergence based on accuracy of matrix reconstruction
        from sparse and low rank parts
        """
        error = np.linalg.norm(Z, 'fro') / x_norm     
        if self.debug:
            print "error = {0}".format(error)
        if self.curr_iter > self.max_iter:
            return True
        else:
            return error <= self.tol

    @staticmethod
    def angle(h):
        return np.arctan2(h.imag, h.real)
# rpca.py ends here
