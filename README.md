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

#### Example 1. Reading folder cotaining multiple datafiles at once

-----------------------------------------------------------------------------------------------------------------------
`import PyMSI as py`

`path = '/home/Documents/data/' # This folder contains 3 sub-folders represent individual MSI data`

`py.AnalyzeData(path,massrange=[],matrix_save='Y',image_plot='Y') `

This command will automatically read data from individual sub-folder. User can define desire mass range, in case of blank default mass range will consider. Default option for matrix_save and image_plot is N, while making them 'Y' each image matrix and corresponding image will save with repsective folder name in path folder.

#### Example 2. Decide mass range by looking at complete mass spectra

-----------------------------------------------------------------------------------------------------------------------

This could be done at two steps: 1) generate mass spectra plot for desired pixel position; 2) looking at spectra plot decide desire mass range and use as input 

`import PyMSI as py`

`import matplotlib.pyplot as plt`

`import numpy as np`

`mass = py.readMSI.readAnalyzet2m('/home/Documents/data/ABX/2009.t2m')`

`intensity = py.PlotSpectra('/home/Documents/data/ABX/2009.img',mass,id = '21',show='N') `
id = interested spectra number, show = 'Y' will save spectra plot in given folder

-Suppose from above spectra plot we are interested in creating ion-intensity image for m/z [289, 290], to be noted it will take value just before 290 i.e. in m/z 290 will be not included, to make include mention one higher m/z value

`spec = readAnalyze('/home/Documents/data/ABX/',massrange =[280,290]) `   extracting data in the form of list

`mat = msiMatrix(spec) `      converting list object into matrix

`Image = mat.matrix `

`Image = np.sqrt(Image)`

`Image = np.ceil(Image)`

`plt.imshow(Image,interpolation='None')`

`plt.show()`





