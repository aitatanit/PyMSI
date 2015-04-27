import numpy as np
import os, sys, struct


## This file contains all the functions used to read
## imaging dataset from different open source file formats


## Analyze7.5 ###################################################################################################################
## The data are stored in three different files: 
## .hdr : the header file contains informations about the image spatial properties 
## .t2m : this file contains the m/z scale of the mass spectra. Note: the mass scale is the same for all the spectra (32 bit Long)
## .img : this file contains the actual intensity values recorded at each position for each m/z value.


## reading the header
def readAnalyzeheader(filename):
   '''Function reading Analyze header file'''
   size = os.stat(filename).st_size
   if((size != 348) & (size != 384)):
       sys.exit("%s file is not Anlayze format.", filename)
   dimensions = np.zeros(8)
   pixdim = np.zeros(8)
   f = open(filename,'rb')
   f.seek(38)
   regular = f.read(1)
   if(regular != 'r'):
       sys.exit("wrong file format")
   f.seek(40)
   for i in range(8):
       dimensions[i] = struct.unpack('H',f.read(2))[0]
   nx = dimensions[2]  # x size of the image (number of columns)
   ny = dimensions[3]  # y size of the image (number of rows)
   f.seek(70)
   datatype = struct.unpack('H',f.read(2))[0]
   bitpix = struct.unpack('H',f.read(2))[0]

   if(datatype == 2 or datatype == 4 or datatype == 8 ):
       what = 'integer'
   elif (datatype == 16 or datatype == 32 or datatype == 64 ):
       what = 'double'
   else:
       what = 'raw'

   signed = (datatype == '2') 
   size = (bitpix/8)
   f.seek(76) 

   for i in range(8):
       pixdim[i] = struct.unpack('f',f.read(4))[0]

   xd = pixdim[1]
   yd = pixdim[2]
   return(nx,ny, xd, yd, signed, size, what) 

## read t2m

def readAnalyzet2m(filename):
	'''Function reading t2m mass file '''
	totalBytes = os.stat(filename).st_size
	bytes = 4
	mass = np.zeros((totalBytes/bytes,1))
	endian = 'f'
	with open(filename,'rb') as f:
		for i in xrange(len(mass)):
			mass[i,0] = struct.unpack(endian,f.read(bytes))[0]
	return mass  


## read img

def readAnalyzeimg(filename,mass,nx,ny,massrange=[]):
        '''Function reading intensity file, input requires mass file and nx ,ny value from readAnalyzeheader function'''
        if (massrange == []):
           mass1, mass2 = min(mass)[0], max(mass)[0]	
        else:
           mass1, mass2 = massrange[0], massrange[1]
        id = (mass >= mass1) & (mass <= mass2)
        index = np.where(id ==True)[0]
        spectra = np.zeros(shape=(index.size, nx *ny))
        spectra1 = np.zeros(shape=(mass.size,1))
        newmassrange = mass[index]
        bytes, endian = 2, 'H'
        with open(filename,'rb') as f:
             for k in range(int(nx)*int(ny)):
                   for i in range(mass.size):
                          spectra1[i,0] = struct.unpack(endian,f.read(bytes))[0]
                   spectra[:,k] = spectra1[index,0]
        return(spectra,newmassrange)



## Wrapper which uses the three previous functions ...






## mzXML  ###################################################################################################################




