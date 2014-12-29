## Class spectrum: low level class which contains mz and I for a single 
## spectrum


import numpy as np


## Small scale classes which identifies one spectrum
class spectrum:
    def __init__(self, mz, intensity):
        ''' Define the spectrum class '''
        self.mz = mz
        self.intensity = intensity
        self.x = 0 
        self.y = 0
