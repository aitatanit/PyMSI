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

## Usage

#### Creating Ion images 

----------------------------------------------------------------------------------------------------------------------
Input required : Folder path, mass range

Output : Ion intensity map, Image and segmentation map matrix in csv file

For folder named Images, containing multiple image dataset folder such as A1, A2, A3.

```javascript
/Documents/MSimaging/Python/PyMSI$ python CreateIonintensityImage.py --file '~/Documents/MSimaging/Images/' -f 284.2 284.3

```

#### Calculate first-order statistics based texture features 

-----------------------------------------------------------------------------------------------------------------------

Input required :  image matrix csv file path

Output : .csv file contains FOS based features value

```javascript
~/Documents/MSimaging$ python Features_Firstorderstatistics.py -f '~/Documents/Msimaging/Images/A1_image.csv'
```                                  
#### Calculate gray-level co-occurence matrix based texture features 

-----------------------------------------------------------------------------------------------------------------------

Input required : image matrix csv file path, distance parameter value

Output : csv file contains GLCM based features value

```javascript
~/Documents/MSimaging$ python Features_Coocurrencematrix.py -f '~/Documents/Msimaging/Images/A1_image.csv -d 1'
``` 
#### Calculate size-zone matrix based texture features

-----------------------------------------------------------------------------------------------------------------------

Input required : image matrix csv file path

Output : csv file contains SZM based features value

Dependency : rpy2 module, and r radiomics library

```javascript
~/Documents/MSimaging$ python Features_SZMbased.py -f '~/Documents/Msimaging/Images/A1_image.csv'
```                                  
#### Calculate shape factors

-----------------------------------------------------------------------------------------------------------------------

Input required : mask_matrix csv file path

Output : csv file contains shape factors value

Dependency : python cv2 module

```javascript
~/Documents/MSimaging$ python Features_Coocurrencematrix.py -f '~/Documents/MSimaging/Images/A1_maski.csv'
``` 


