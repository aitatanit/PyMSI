### msiMatrix : this class represent MSI data cube i.e. mass spectra at x and y co-ordinate.
### The constructor requires:
##    - a list of mass spectra
##    - [x,y] dimensions of raster
### output returned : data cube with spectra at each x,y point and mass vector




class msiCube:
  def __init__(self,speclist,dims):
    '''Constructor for msiCube class'''
    m = speclist.spectra[1]
    self.mz = m.mz
    self.cube = np.zeros([m.mz.size,dims[1],dims[0]])
    for s in speclist.spectra:
        self.cube[s.x,s.y,:]= s.intensity
  def __call__(self):
    return (self.cube,self.mz)    
