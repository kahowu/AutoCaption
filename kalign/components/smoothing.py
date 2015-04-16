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
    def __init__(self, threshold=0.01, yst=20, K=5):
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
        #xT_smooth = np.int_(sgm)
        x[np.logical_not(sgm)] = 0
        
        # t = range(1, x.shape[0] + 1)
        # plt.plot(t, sgm, linewidth=3)
        # plt.show()
        # import pdb; pdb.set_trace();
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
