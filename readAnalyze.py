import numpy as np
import pylab as plt
import os, sys, struct
import matplotlib

class readanalyze():
  
    def __init__(self):
      self.path = self.readfile()
       
    def readfile(self):
      '''Function to pass analyze folder path'''
      path = '/home/mridula/Documents/MSimaging/FromPietero/MSImaging/sub/AREA/'
      
      '''while 1:
        path = raw_input("Enter analyze files folder path : ")
        if path == "":
           print "Retry"
        else:
	   print "Path ", path
	   break'''
           
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
      filename1 = path+filename1
      filename2 = path+filename2
      filename3 = path+filename3            
	   
      return(filename1,filename2,filename3)
      
    def readheader(self,filename):
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
       self.nx = dimensions[2]
       self.ny = dimensions[3]
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
       return(self.nx,self.ny, xd, yd, signed, size, what) 
     
    def readmass(self,filename):
        '''Function reading t2m mass file '''
        totalBytes = os.stat(filename).st_size
        bytes = 4
	self.mass = np.zeros((totalBytes/bytes,1))
	endian = 'f'
	with open(filename,'rb') as f:
            for i in xrange(len(self.mass)):
                self.mass[i,0] = struct.unpack(endian,f.read(bytes))[0]
	return self.mass  
      
    def readintensity(self,filename,mass,nx,ny):
        '''Function reading intensity file, input required mass file and nx ,ny value, which shows number of spectra in
        MSI data. Here user can define mass range to get spectra for specific mass range'''
        userinput = raw_input("User want to define mass range : Y or N : ")
        if (userinput == 'Y'):
           massrange= [x for x in raw_input("Enter mass range in comma separated form: ").split(',')]
           mass1, mass2 = int(massrange[0]), int(massrange[1])
        else:
           mass1, mass2 = min(self.mass)[0], max(self.mass)[0]
        id = (self.mass >= mass1) & (self.mass <= mass2)
        index = np.where(id ==True)[0]
        self.spectra = np.zeros(shape=(index.size, self.nx *self.ny))
        spectra1 = np.zeros(shape=(self.mass.size,1))
        newmassrange = self.mass[index]
        bytes, endian = 2, 'H'
        with open(filename,'rb') as f:
             for k in range(self.nx*self.ny):
                   for i in range(self.mass.size):
                          spectra1[i,0] = struct.unpack(endian,f.read(bytes))[0]
                   self.spectra[:,k] = spectra1[index,0]
        return(self.spectra,newmassrange)


class Spectrum(readanalyze):
    '''Class reading MSI data'''
    def __init__(self):
      self.path = self.readfile()
      self.header = self.readheader(self.path[0])
      self.nx = int(self.header[0])
      self.ny = int(self.header[1])
      self.mass = self.readmass(self.path[1])
      self.output = self.readintensity(self.path[2],self.mass,self.nx,self.ny)
      self.intensity = self.output[0]
      self.massrange = self.output[1]
      self.Msimatrix = np.concatenate((self.output[1],self.output[0]),axis=1)
    def __call__(self):  
      pass 
    def radq(self,intensity):
      '''Perform square root transformation of intensity file'''
      intensity = np.sqrt(intensity)
      return intensity
    def ticnorm(self,intensity):
      '''Perform total ion current normalisation'''
      for i in range(intensity.shape[1]):
	   intensity[:,i] = intensity[:,i]/sum(intensity[:,i])     
      return intensity   
    def convert(self,m):
      '''Convert analyze 7.5 object into speclist object; input required is m object from Spectrum class'''
      self.ms = np.zeros(m.intensity.shape[1])
      self.ms = list(self.ms)
      for i in range(len(self.ms)):
         self.ms[i] = np.zeros(shape=(m.mass.size,2))
         self.ms[i][:,0] = m.mass[:,0]
         self.ms[i][:,1] = m.intensity[:,i] 
      return self.ms
    
class MSI:
    '''Class MSI to return MSI image as an output. Input required is Intensity matrix and image x, y co-ordinate. Information
       regarding image x,y co-ordinate can obtain from the header file'''
    def __init__(self,intensity,nx,ny):
      self.image = np.zeros(shape=(nx,ny))
      ys = np.repeat(range(0,ny),nx)
      xs = np.repeat(range(0,nx),ny)
      xs = xs.reshape((nx,ny))
      xs = xs.flatten('F')
      for k in range(nx * ny):
	   self.image[xs[k],ys[k]] = np.sum(intensity[:,k])
    def __call__(self):   
      return self.image
 

       
     
