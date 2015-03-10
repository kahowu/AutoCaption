# component.py --- 
# 
# Filename: component.py
# Description: 
# Author: Jonathan Chung
# Maintainer: 
# Created: Thu Mar  5 20:23:57 2015 (-0500)
# Version: 
# Package-Requires: ()

from data import Kdatabase
from data import Kdata

# Code:
class Kcomponent():
    '''
    docs
    '''
    def __init__(self):
        pass

    def run(self, kdatas):
        if isinstance(kdatas, Kdatabase):
            for kdata in kdatas:
                self.component(kdata)
        else:
            kdata = kdatas
            self.component(kdata)

# component.py ends here
