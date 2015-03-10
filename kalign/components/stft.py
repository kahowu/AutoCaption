# stft.py --- 
# 
# Filename: stft.py
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
import numpy as np
from utils.pyNumpyViewer import pyNumpyViewer

class Stft(Kcomponent):
    '''
    docs
    '''
    def __init__(self, lamb=1, nfft=1024, overlap=4, scf=0.666):
        self.name = "stft"
        self.lamb = lamb
        self.nfft = nfft
        self.hop = nfft / overlap
        self.scf = scf
        
    def component(self, kdata):
        w = hamming(self.nfft + 1)[:-1]
        x = kdata["input"]
        X = self.scf * np.array([np.fft.rfft(w*x[i:i + self.nfft]) for i in range(0, len(x) - self.nfft, self.hop)])
        kdata[self.name] = X

# stft.py ends here
