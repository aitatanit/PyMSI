import numpy as np
import os, sys, struct
from PyMSI.speclist import speclist 
## This file contains all the functions used to read
## imaging dataset from different open source file formats


## Analyze7.5 ###################################################################################################################
## The data are stored in three different files: 
## .hdr : the header file contains informations about the image spatial properties 
## .t2m : this file contains the m/z scale of the mass spectra. Note: the mass scale is the same for all the spectra (32 bit Long)
## .img : this file contains the actual intensity values recorded at each position for each m/z value.


## reading the header
def readAnalyzeheader(filename):
   '''Function reading Analyze header file
   
   The header contains informations regardin gthe number of 
   points and other dataset characteristics.

   Args:
   filename : The name of the hdr file

   Value:
   nx : number of pixels in th x direction
   ny : number of pixel in the y direction
   xd : step in x 
   xy : step in y
   '''
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
   return(int(nx),int(ny), xd, yd, signed, size, what) 

## read t2m

def readAnalyzet2m(filename):
	'''Function reading t2m mass file '''
	totalBytes = os.stat(filename).st_size
	bytes = 4
	mass = np.zeros(totalBytes/bytes)
	endian = 'f'
	with open(filename,'rb') as f:
		for i in xrange(len(mass)):
			mass[i] = struct.unpack(endian,f.read(bytes))[0]
	return np.array(mass)  


## read img

def readAnalyzeimg(filename,mass,nx,ny,massrange = []):
  '''Function reading intensity file, it requires the mass file as an input.
  The user can define mass range to get spectra for specific mass range
  '''
  if (massrange == []):
    mass1, mass2 = min(mass), max(mass)
  else:
    mass1, mass2 = massrange[0], massrange[1]
  id = (mass >= mass1) & (mass <= mass2)
  ## we want to return a list of 2D arrays like the speclist
  mylist = []     ## empty list to store the spectra
  bytes, endian = 2, 'H'
  with open(filename,'rb') as f:
    for k in range(int(nx)*int(ny)):
      spcarr = np.zeros(len(mass))
      for i in range(mass.size):
        if not id[i]:
          f.seek(bytes,1)
          continue 
        test = struct.unpack(endian,f.read(bytes))[0]
        spcarr[i] = test
      print("Processing Spectrum " + str(k))
      spectrum = np.vstack([mass,spcarr]).transpose()
      mylist.append(spectrum[id,:])
  return(mylist)


## Wrapper which uses the three previous functions ...

def readAnalyze(filename, massrange = []):
  ''' Read a MSI dataset in Analyze 7.5  format

  Args:
  filename: a string with the name of the dataset without extension
  massrange: a list specifying the mass range to be imported [mzmin,mzmax]

  Return:
  An object of class speclist
  '''
  path = path
  massrange = massrange
  dirs = os.listdir(path)
  for file in dirs:
      if (file.endswith('.hdr') == True):
         filename1 = file
      if (file.endswith('.t2m') == True):
         filename2 = file
      if (file.endswith('.img') == True):
         filename3 = file
     
  if(filename1 == "" or filename2 == "" or filename3 == ""):
         sys.exit("Incomplete analyze folder found")
  stre = "/"
  f1 = (path,filename1); filename1 = stre.join(f1)
  f2 = (path,filename2); filename2 = stre.join(f2)
  f3 = (path,filename3); filename3 = stre.join(f3)
 
  print("Reading the Header infos \n")
  header = readAnalyzeheader(filename1)
  print("Image size: " + str(header[0]) + "*" + str(header[1]) + " \n")
  mass = readAnalyzet2m(filename2)
  print("Reading the Spectra")
  mylist = readAnalyzeimg(filename3, mass, header[0], header[1], massrange)
  ## format it as a speclist object
  output = speclist(mylist,[header[0], header[1]])
  return(output)






## mzXML  ##########################################################################




