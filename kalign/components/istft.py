# istft.py --- 
# 
# Filename: istft.py
# Description: 
# Author: Jonathan Chung
# Maintainer: 
# Created: Sun Mar  8 10:11:37 2015 (-0400)
# Version: 
# Package-Requires: ()

# Code:
from component import Kcomponent
from scipy import hamming
from scipy import fft
from scipy import real
import numpy as np

class Istft(Kcomponent):
    '''
    docs
    '''
    def __init__(self, lamb=1, nfft=1024, overlap=4, scf=0.666):
        self.name = "istft"
        self.lamb = lamb
        self.nfft = nfft
        self.hop = nfft / overlap
        self.scf = scf
        
    def component(self, kdata):
        X = kdata["rpca_l"]

        fftsize = self.nfft
        w = hamming(fftsize + 1)[:-1]
        x = np.zeros(X.shape[0] * self.hop)
        wsum = np.zeros(X.shape[0] * self.hop)
        for n,i in enumerate(range(0, len(x)-fftsize, self.hop)):
            x[i:i + fftsize] += real(np.fft.irfft(X[n])) * w
            wsum[i:i + fftsize] += w ** 2.
        pos = wsum != 0
        x[pos] /= wsum[pos]
        x = x.astype(np.int16)
        kdata[self.name] = x

# istft.py ends here
