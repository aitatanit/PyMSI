'''
For folder named Images, containing multiple image dataset folder such as A1, A2, A3.
Command line argument will be : 
/Documents/MSimaging/Python/PyMSI$ python CreateIonintensityImage.py --file '~/Documents/MSimaging/Images/' -f 284.2 284.3
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,"~/Documents/MSimaging/Python/PyMSI")
import readMSI
import msiMatrix
from scipy import misc
from scipy import ndimage
from PIL import Image
import matplotlib.pyplot as plt
import os, struct
import numpy as np
from skimage import filter
import argparse
from speclist import speclist 


def getidmaxIntensity(filename,mass):
    spectra = np.zeros(shape=(mass.size))
    f = open(filename,'rb')
    f.seek(mass.size * int(20) * 2)
    for i in xrange(mass.size):
        spectra[i] = struct.unpack('H',f.read(2))[0]
    nu =  np.where(spectra == max(spectra))
    nu = nu[0][0]
    return(nu)

def creatImage(address,massrange=[]):
    dirs = os.listdir(address)        
    ### Create ion intensity image for maximum intensity value from bkg region. It will use to create mass
    for f in dirs:
        if (f.endswith('.img') == True):
           fileimage = f
        if (f.endswith('.t2m') == True):
           filemass = f
        if (f.endswith('.hdr') == True):
	   fileheader = f
    stre = "/"
    f1 = (address,fileimage); file1 = stre.join(f1)
    f2 = (address,filemass); file2 = stre.join(f2)
    f3 = (address,fileheader); file3 = stre.join(f3)
    mass = readMSI.readAnalyzet2m(file2)                      ## read mass file
    header = readMSI.readAnalyzeheader(file3)                ##read header information
    ind = getidmaxIntensity(file1,mass)                      ## find mz index for maximum intensity/peak value
    mass1 = mass[ind]-0.8; mass2 = mass[ind]+0.8
    specbkg =  readMSI.readAnalyzeimg(file1,mass,header[0],header[1],[mass1,mass2])    ## creating ion intensity image for above mz
    output = speclist(specbkg,[header[0], header[1]])
    mat = msiMatrix.msiMatrix(output)
    Imgbkg = mat.matrix 
    Imgbkg = np.sqrt(Imgbkg)
    Imgbkg = np.ceil(Imgbkg)
    Imgbkg = ndimage.median_filter(Imgbkg,3)
    val = filter.threshold_otsu(Imgbkg)
    mask = Imgbkg < val        
    #### Create drug image 
    specdrug = readMSI.readAnalyzeimg(file1,mass,header[0],header[1],massrange)
    output1 = speclist(specdrug,[header[0], header[1]])
    maat = msiMatrix.msiMatrix(output1)
    Imgdrug = maat.matrix
    Imgdrug = np.sqrt(Imgdrug)
    Imgdrug = np.ceil(Imgdrug)        
    ### Creating drug mask image
    imgf = []; imgf1 = []
    maskf = mask.flatten()
    Img = Imgdrug.flatten()
    for i in range(len(maskf)):
        if maskf[i] == True:
           imgf.append(Img[i])        
    imgf = np.asarray(imgf)
    dat = np.unique(imgf)
    result = np.zeros(shape=(Imgdrug.shape))
    for x in range(0,Imgdrug.shape[0]):
        for y in range(0,Imgdrug.shape[1]):
            if mask[x,y] == False:
               result[x,y] = (52)
            else:
               result[x,y] = ((Imgdrug[x,y] - np.min(dat)) *((50 - 1)/ (np.max(dat) - np.min(dat)))) + 1
               imgf1.append(result[x,y])        
    result = np.ceil(result)
    result = ndimage.median_filter(result,3)    
    return(result,mask)

def main():    
    parser = argparse.ArgumentParser(description="Creat ion intensity image with uniform background")
    parser.add_argument('--file',dest ="fpath",action='store', help = "Folder path containing MSI dataset")
    parser.add_argument('-f',dest = "massrange",type = float,nargs ='+',default=[],help = "desired m/z range")
    args = parser.parse_args()
    path = args.fpath
    path = path.strip()
    massrange = args.massrange
    listing = os.listdir(path)
    for im in range(0,len(listing)):
        address = path + listing[im]
        print("Reading filename " + str(listing[im]))
        Image,mask = creatImage(address,massrange=[])
        outputi = path + listing[im] + '_image.csv'
#        outputi = path + listing[im] + '_image.csv' '{} {} _image.csv' .format(path,listing[im])
        outputm = path + listing[im] + '_maski.csv'
        outputf = path + listing[im] + '.jpg'
        np.savetxt(outputi,Image,fmt='%-7.5f',delimiter=',')
        np.savetxt(outputm,mask,fmt='%-3.2f',delimiter=',')
        plt.imshow(Image,interpolation='None')
        plt.colorbar()
        plt.savefig(outputf,bbox_inches='tight')
        
                
if __name__ == '__main__':
   main()
