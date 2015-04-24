PyMSI
=====
Collection of python tools for the analysis of Mass Spectrometry Imaging datasets

## Accepted File Formats
The module provides function to load the data stored in the following formats. 

Analyze7.5
The data are stored in three different files: 
- .hdr : the header file contains informations about the image spatial properties 
- .t2m : this file contains the m/z scale of the mass spectra. Note: the mass scale is the same for all the spectra (32 bit Long)
- .img : this file contains the actual intensity values recorded at each position for each m/z value.



## Module Structure
The module is organized around the following classes:

1. spectrum: low level class which contains mz and I for a single spectrum.
2. speclist: this class represent a collection of spectra with the associated x y coordinates. The constructor requires:
	* a list of mass spectra
	* an optional [x,y] dimensions of the raster 
	* a string representing the geometry of the acquisition. either "S" for meandering or "N" for simple row-wise acquisition
