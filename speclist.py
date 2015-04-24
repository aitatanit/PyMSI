## speclist: this class represent a collection of spectra with
## the associated x y coordinates. The constructor requires:
## -  a list of mass spectra
## -  an optional [x,y] dimensions of the raster 
## -  an  optional string representing the geometry of the acquisition. 
##    Either "S" for meandering or "N" for row-wise acquisition

import numpy as np
from copy import deepcopy

class speclist:
    def __init__(self,mylist,dims = [], geom = "N"):
        ''' Construct the speclist class from the inputs'''
        self.spectra = [spectrum(x) for x in mylist]
        if (dims != []):
            ys = np.repeat(range(0,dims[1]),dims[0])
            xs = np.repeat(range(0,dims[0]),dims[1])
            xs = xs.reshape((dims[0],dims[1]))
            if (geom == "S"):
        	   xs[:,range(1,dims[1],2)] = xs[::-1,range(1,dims[1],2)]
            xs = xs.flatten('F')
            for i in range(0,len(self.spectra)):
                self.spectra[i].x = xs[i]
                self.spectra[i].y = ys[i]
    def __getitem__(self,index):
        return self.spectra[index] 
    def slice(self,window):
        ''' Create a new speclist with reduced mass range (mzmin,mzmax)'''
        newspec = deepcopy(self)
        for s in newspec.spectra:
        	idin = (s.mz < window[1]) & (s.mz > window[0])
        	s.mz = s.mz[idin]
        	s.intensity = s.intensity[idin]
        return(newspec)
    def ticnorm(self):
        ''' Perfor a total ion current normalization of the spectra'''
        for i in range(0,len(self.spectra)):
            self.spectra[i].intensity = self.spectra[i].intensity/sum(self.spectra[i].intensity)
   