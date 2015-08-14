PyMSI
=====
Collection of python tools for the analysis of Mass Spectrometry Imaging datasets

## Accepted File Formats
The module provides function to load the data stored in the following formats. 

Analyze7.5
The data are stored in three different files: 
* .hdr : the header file contains informations about the image spatial properties 
* .t2m : this file contains the m/z scale of the mass spectra. Note: the mass scale is the same for all the spectra (32 bit Long)
* .img : this file contains the actual intensity values recorded at each position for each m/z value.



## Module Structure
The module is organized around the following classes:

1. spectrum: low level class which contains mz and I for a single spectrum.
2. speclist: this class represent a collection of spectra with the associated x y coordinates. The constructor requires:
	* a list of mass spectra
	* an optional [x,y] dimensions of the raster 
	* a string representing the geometry of the acquisition. either "S" for meandering or "N" for simple row-wise acquisition

## Working with PyMSI module:

#### Example 1. Import folder containing multiple data files and save them 

-----------------------------------------------------------------------------------------------------------------------
```javascript
import PyMSI as py      
// load module into variable py

path = '/home/Documents/data/'  // define folder path. Here data folder contains 3 sub-folders represent different MSI data
   
py.AnalyzeData(path,massrange=[],matrix_save='Y',image_plot='Y') 

```

AnalyzeData command used to read and save data. Input requires to this command is: folder path, desired m/z range (in case of blank complete m/z scale will be considered), matrix_save to save image matrix as csv file and image_plot to save ion-intensity image for each dataset. 

To save data folder name will use as file name.


#### Example 2. Plot complete mass spectra and then create ion-intensity map

-----------------------------------------------------------------------------------------------------------------------

This could be done in two steps: 
1) generate mass spectra plot for desired pixel position
2) in spectra plot decide mass range of interest and use that as an input for image creation

* step 1

```javascript
import PyMSI as py

import matplotlib.pyplot as plt    
// default python package required to make plot

import numpy as np

mass = py.readMSI.readAnalyzet2m('/home/Documents/data/ABX/2009.t2m') // read mass file

intensity = py.PlotSpectra(path = '/home/Documents/data/ABX/2009.img',mass= mass,id = '21',showspectra='Y') 

plt.plot(mass,intensity)

plt.show()
```                                  

py.PlotSpectra command used to make spectrum plot and save intensity value into variable called intensity. Input required: path = path of image file, mass = variable contains m/z data, id = interested spectra number, showspectra = 'Y' will plot spectra on screen

* step 2

Suppose from above spectrum plot we are interested in creating ion-intensity image for mass range [289, 290] we will follow commands given below:

```javascript
spec = readAnalyze('/home/Documents/data/ABX/',massrange =[280,290])   
 //read data as list with two element: mass, intensity
 
mat = msiMatrix(spec)     // converting list object into image matrix                                            

Image = mat.matrix 

Image = np.sqrt(Image)

plt.imshow(Image,interpolation='None')

plt.show()
```
> Note : while defining mass range as [280,290] will take values from 280 to just before 290. To make 290 acceptable give one higher index.  



