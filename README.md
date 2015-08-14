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
`import PyMSI as py`

`path = '/home/Documents/data/'

`py.AnalyzeData(path,massrange=[],matrix_save='Y',image_plot='Y') `

First line command load module into variable py
In the second line path of folder defined. Here data folder contains 3 sub-folders represent different MSI data
Final in third line AnalyzeData command used. Input requires to this command is: folder path, desired m/z range (in case of blank complete m/z scale will be considered), matrix_save to save image matrix as csv file and image_plot to save ion-intensity image for each dataset. 
To save data folder name will use as file name.


#### Example 2. Plot complete mass spectra and then create ion-intensity map

-----------------------------------------------------------------------------------------------------------------------

This could be done in two steps: 
1) generate mass spectra plot for desired pixel position
2) in spectra plot decide mass range of interest and use that as an input for image creation

*step 1
`import PyMSI as py`

`import matplotlib.pyplot as plt`

`import numpy as np`

`mass = py.readMSI.readAnalyzet2m('/home/Documents/data/ABX/2009.t2m')`

`intensity = py.PlotSpectra(path = '/home/Documents/data/ABX/2009.img',mass= mass,id = '21',showspectra='Y') `
                                  

From step 1 to 3 we are loading required packages.
py.readMSI.readAnalyzet2m command used to read mass data
py.PlotSpectra command used to plotspectra and save intensity value into variable called intensity. Inputs required here are: path = path of image file, mass = variable contains m/z data, id = interested spectra number, showspectra = 'Y' will plot spectra on screen

*step 2

Suppose from above spectra plot we are interested in creating ion-intensity image for m/z [289, 290] we will do as commands given below.

`spec = readAnalyze('/home/Documents/data/ABX/',massrange =[280,290]) `   extracting data in the form of list

`mat = msiMatrix(spec) `                                                   converting list object into matrix

`Image = mat.matrix `

`Image = np.sqrt(Image)`

`Image = np.ceil(Image)`

`plt.imshow(Image,interpolation='None')`

`plt.show()`





