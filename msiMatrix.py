## msiMatrix : this class represent MSI 2-Dmatrix, contstructed through summation of 
##  intensity value at each spatial dimension. The constructuctor requires:
## - a list of mass spectra
## - [x,y] dimensions of raster

from PyMSI.speclist import speclist 
import numpy as np

class msiMatrix:
  def __init__(self,speclist):
    '''Construct the msiMatrix class from inputs

    The msiMatrix is basically only a 2D Numpy array 

    Args: 
    speclist : an object of class speclist with explicit coordinates
    '''
    nx = max([s.x for s in speclist.spectra])+1
    ny = max([s.y for s in speclist.spectra])+1
    self.matrix = np.zeros([nx,ny])
    for s in speclist.spectra:
        self.matrix[s.x,s.y] = sum(s.intensity)
  def __call__(self):
    return self.marix
  

