# smoothing.py --- 
# 
# Filename: smoothing.py
# Description: 
# Author: Jonathan Chung
# Maintainer: 
# Created: Tue Apr 14 09:50:07 2015 (-0400)
# Version: 
# Code:

from component import Kcomponent
import maxflow
from pyNumpyViewer import pyNumpyViewer as PNV
import matplotlib.pyplot as plt
import numpy as np

class Smoothing(Kcomponent):
    '''
    docs
    '''
    def __init__(self, debug=False, threshold=0.10, yst=20, K=5):
        self.debug = debug
        self.threshold = threshold
        self.yst = yst
        self.K = K
    
    def component(self, kdata):
        x = kdata["vocal"]
        g = maxflow.Graph[float]()

        nodeids = g.add_nodes(x.shape[0])
        for (t, nodeid, nodeid_1) in zip(x, nodeids, nodeids[1:]):
            g.add_edge(nodeid, nodeid_1, self.yst, self.yst)
            cost0, cost1 = self.cost(t)
            g.add_tedge(nodeid, cost0, cost1)

        g.maxflow()
        sgm = g.get_grid_segments(nodeids) # is max flow connected to source
                
        if self.debug:
            t = np.arange(1, x.shape[0] + 1)/16000.00
            plt.subplot(2, 1, 1)
            plt.plot(t, x)
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude")
            plt.subplot(2, 1, 2)
            plt.plot(t, sgm, linewidth=3)
            plt.xlabel("Time (s)")
            plt.ylabel("Vocal gate")
            plt.show()
            
        x[np.logical_not(sgm)] = 0
  
        kdata["smoothedVocal"] = x
             
    def cost(self, t):
        ## How likely is this to be 0 or 1 given the current value
        ## if intensity is small then more likely to be 0
        L = 1
        x0 = self.threshold
        k = self.K
        t = abs(t)
        logistic = L / (1 + np.exp(-k * (t - x0))) 
        cost0 = 1 - logistic
        cost1 = logistic  
        return cost0, cost1
    
# smoothing.py ends here
