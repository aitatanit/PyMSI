## msiMatrix : this class represent MSI 2-Dmatrix, contstructed through summation of 
##  intensity value at each spatial dimension. The constructuctor requires:
## - a list of mass spectra
## - [x,y] dimensions of raster

class msiMatrix:
  def __init__(self,speclist,dims):
    '''Construct the msiMatrix class from inputs'''
    self.matrix = np.zeros([dims[1],dims[0]])
    for s in speclist.spectra:
        self.matrix[s.y,s.x] = sum(s.intensity)
  def __call__(self):
    return self.marix
  
