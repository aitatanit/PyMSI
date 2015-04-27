## Class spectrum: low level class which contains mz and I for a single 
## spectrum
## column[0] is mz
## column[1] is I

import numpy as np


## Small scale classes which identifies one spectrum
class spectrum:
    def __init__(self, m):
        ''' Define the spectrum class 

        A Spectrum is a 2D array with mz and intensity properties
        Since this class is mainly used for imaging applications
        it includes x and y properties.

        Args:
         m (list): 2D list with mz and I values.
        '''
        pippo = np.array(m)
        self.mz = pippo[:,0]
        self.intensity = pippo[:,1] 
        self.x = 0 
        self.y = 0
    def slice (self,window):
        ''' Slice a spectrum 

        Method to subset the mz range of a spectrum object

        Args:
        window = [mzmin,mzmax]: 2D list with mz limits
        '''
        idin = (self.mz < window[1]) & (self.mz > window[0])
        self.mz = self.mz[idin]
        self.intensity = self.intensity[idin]   
