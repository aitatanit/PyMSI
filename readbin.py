from numpy import *
import os
import struct
import matplotlib
import pylab as plt

def readt2mfile(filename,bytes=4,endian='f'):
    totalBytes = os.stat(filename).st_size
    values = empty((totalBytes/bytes,1))
    with open(filename,'rb') as f:
        for i in xrange(len(values)):
            values[i,1] = struct.unpack(endian,f.read(bytes))[0]
    return values

def readintfile(filename,bytes=2,endian='H'):
    totalBytes = os.stat(filename).st_size
    values = empty((29695,5000))
    with open(filename,'rb') as f:
 	      for k in range(5000):
		      for i in range(29695):   
				values[i,k] = struct.unpack(endian,f.read(bytes))[0]
		      
    return values
	 
    

mass = readt2mfile('200913.t2m')
img = readintfile('200913.img')

plt.plot(mass,img)
plt.plot(mass,img[:,1:5])
plt.show()

id = (mass >270) & (mass <271)
im1 = img[id,:]
im2 = sum(im1,axis = 1)
mass1 = mass[id]

spectra = concatenate((mass1,im1),1)

plt.plot(spectra[:,0],spectra[:,1:500])

spectra1 = concatenate((mass1,im2),1)


#########################################################################

def readintfile(filename,bytes=2,endian='H'):
    spectra = empty((29695,5))
    with open(filename,'rb') as f:
      for j in range(5):
	  for i in range(29695):
	      spectra[i,j] <- struct.unpack(endian,f.read(bytes))[0]
    return spectra


%load_ext rpy2.ipython 
%R load("/home/mridula/Documents/MSimaging/COMP/MSIQuery-try/readAnalyzeHdr1.R")
%R path <- "/home/mridula/Documents/MSimaging/FromPietero/MSImaging/Uniformità/PTX #139_D3_SPRAY/200913.hdr"
%R head <- readAnalyzeHdr1(path)

## In R spectra is a list of S4 objects ...
%R nx <- head$nx; ny <- head$ny 


## <------- The best should be to store the spectra into a list of dictionaries
## here i get the spectralist in my python space
%Rpull -d nx ny