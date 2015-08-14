''' Function PlotSpectra : to plot complete mass spectra for given index,
    Function AnalyzeData : Take Folder path as input which contains several sub-folder as MSI data''' 


from PyMSI.readMSI import readAnalyze
from PyMSI.msiMatrix import msiMatrix
import matplotlib.pyplot as plt
import os
import numpy as np
import struct

def PlotSpectra(mass,filename,id= '10',showspectra='N'):
     spectra = np.zeros(shape=(mass.size))
     f = open(filename,'rb')
     f.seek(mass.size * int(id) * 2)
     for i in xrange(mass.size):
       spectra[i] = struct.unpack('H',f.read(2))[0]
     if(showspectra == 'Y'):
        plt.plot(mass,spectra) 
        plt.show()
     return(spectra)

def AnalyzeData(path,massrange=[],matrix_save ='N',image_plot='N'):
    listing = os.listdir(path)
    for im in range(0,len(listing)):
        address = path+listing[im]
        print("Reading filename "+ str(listing[im]))
        spec = readAnalyze(address,massrange)
        mat = msiMatrix(spec)
        Image = mat.matrix 
        Image = np.sqrt(Image)
        Image = np.ceil(Image)
        if(matrix_save == 'Y'):
           outputf = path+listing[im]+'.csv'
           np.savetxt(outputf,Image, fmt='%-7.5f',delimiter=",")
        if(image_plot == 'Y'):
           outputp = path+listing[im]+'.jpg'
           plt.imshow(Image,interpolation='None')
           plt.savefig(outputp,bbox_inches='tight')
