
# drfinition of two classes, spectrum and spectrumlist with their methods 

import numpy as np
from copy import deepcopy
import scipy
import pylab as plt
from skimage import transform as tf
from skimage.draw import polygon

## to use the r2py interface and the MaldiQuantForeign to get the data
import rpy2.robjects as robjects
robjects.r('library(MALDIquantForeign)')


def getimportMS():
    robjects.r('library(MALDIquantForeign)')
    robjects.r(''' 
        importMS <- function(path,...){
        spectra <- import(path, ...)
        spectralist <- lapply(spectra, function(x) {as.matrix(cbind(x@mass,x@intensity))})
        return(spectralist)
        }
        ''')
    r_importMS = robjects.r('importMS')
    return(r_importMS)
r_importMS = getimportMS()



## Small scale classes which identifies one spectrum
class Spectrum:
    def __init__(self, m):
        ''' Define the spectrum class '''
        pippo = np.array(m)
        self.mz = pippo[:,0]
        self.intensity = pippo[:,1] 
    def slice (self,window):
        ''' Slice a spectrum '''
        idin = (self.mz < window[1]) & (self.mz > window[0])
        self.mz = self.mz[idin]
        self.intensity = self.intensity[idin]

## For MSI one has to deal with list of spectra, each element
## is identified by a x,y position
## some methods for normalization and scaling are also included
class Speclist:
    def __init__(self,mylist):
        ''' A list of spectra'''
        self.spectra = [Spectrum(x) for x in mylist]
    def __getitem__(self,index):
        return self.spectra[index]
    def slice(self,window):
        ''' Slice a Speclist with a window (mzmin,mzmax)'''
        for s in self.spectra:
            s.slice(window)
    def addcoordinates(self,xscans,yscans):
        ''' Add the coordinates to each spectrum '''
        ys = np.repeat(range(0,yscans),xscans)
        xs = np.repeat(range(0,xscans),yscans)
        xs = xs.reshape((xscans,yscans))
        xs[:,range(1,yscans,2)] = xs[::-1,range(1,yscans,2)]
        xs = xs.flatten('F')
        for i in range(0,len(self.spectra)):
            self.spectra[i].x = xs[i]
            self.spectra[i].y = ys[i]
    def radq(self):
        ''' Performa square root transforamtion of all the spectra'''
        for i in range(0,len(self.spectra)):
            self.spectra[i].intensity = np.sqrt(self.spectra[i].intensity)
    def ticnorm(self):
        ''' Perfor a total ion current normalization of the spectra'''
        for i in range(0,len(self.spectra)):
            self.spectra[i].intensity = self.spectra[i].intensity/sum(self.spectra[i].intensity)


## A 2D image representing the spatial distribution of a 
## mass interval 
class MSI:
    def __init__(self,speclist,xscans,yscans):
        ''' Construct a 2D array from a Speclist'''
        self.image = np.zeros([yscans,xscans])
        for s in speclist.spectra:
            self.image[s.y,s.x] = sum(s.intensity)
    def __call__(self):
        return self.image




## These two classes define Region of interests and 
## implement the tools to manually identify them on 
## one image plot
class RoiList:
    def __init__(self, mylist):
        ''' List of coordinates of the region of interest '''
        self.rois = mylist
    def __getitem__(self,index):
        return self.rois[index]


class RoiCreator:
    def __init__(self,fig,image):
        ''' Handles the events to create interactively the regions of interset. '''
        self.ax = fig.gca()    ## returns the active axis instance
        self.ys = []
        self.xs = []
        self.rois = []
    def event_method(self, event):
        ''' Event handler for the interactively creation of the region of interest '''
        ## want to pick points only if nothing is selected in the toolbar ...
        toolbar = plt.get_current_fig_manager().toolbar  
        if toolbar.mode =='':
            self.ys.append(round(event.ydata))
            self.xs.append(round(event.xdata))
            if event.button == 1:
                col = 'Lime'
            if event.button != 1:
                col = 'Red'
            self.ax.scatter(self.xs,self.ys, s = 30, c = col)
            plt.draw()
            if event.button != 1:
                self.rois.append(np.vstack([np.array(self.xs),np.array(self.ys)]))
                self.ys = []
                self.xs = []
    def getroilist(self):
        return RoiList(self.rois)

## From ROIs is possible to identify masks which represent 
## the areas included in the rois over a specific image
## the projection of masks with an affine transformation
## is also possible

class Masks:
    def __init__(self,roilist,image):
        ''' Construct a list of ROI masks'''
        self.image = image
        self.masks = []
        for roi in roilist:
            empty = np.zeros(image.shape, dtype=np.uint8)
            rr,cc = polygon(roi[1,:],roi[0,:])
            empty[rr, cc] = 1 
            self.masks.append(empty)
    def __getitem__(self,index):
        return self.masks[index]
    def warpmasks(self,tform,imagetarget):
        ''' Warps the masks by using tform on the target image '''
        for i in range(0,len(self.masks)):
            newmask = tf.warp(self.masks[i], tform.inverse, order = 0, output_shape = imagetarget.shape)
            self.masks[i] = newmask/newmask.max()
        self.image = imagetarget
    def getintensity(self,image):
        ''' Returns a list of the intensities of the image on the list of masks'''
        ids = [mask > 0 for mask in self.masks]
        return [image[id] for id in ids]



## Two classes which take care of image registration
## hooks keeps corresponding points in the destination and source
## the class hooks creator takes care of the interactive selecion of the points

class Hooks:
    def __init__(self,src,dst):
        self.src = src
        self.dst = dst


class HookCreator:
    def __init__(self,srcaxes,dstaxes):
        self.srcaxes = srcaxes
        self.dstaxes = dstaxes
        self.old_x = []
        self.old_y = []
        self.new_x = []
        self.new_y = []
        self.sub = []
        self.src = []
        self.dst = []
    def over_method(self,event):
        self.sub = event.inaxes
    def click_method(self, event):
        ## want to pick points only if nothing is selected in the toolbar ...
        toolbar = plt.get_current_fig_manager().toolbar  
        if toolbar.mode =='':
            if self.sub == self.srcaxes:
                self.old_x.append(round(event.xdata))
                self.old_y.append(round(event.ydata))
                self.srcaxes.scatter(self.old_x,self.old_y, s = 40, c = 'Lime')
                plt.draw()
                if event.button != 1:
                    self.src.append(np.transpose(np.vstack([np.array(self.old_x),np.array(self.old_y)])))
            if self.sub == self.dstaxes:
                self.new_x.append(round(event.xdata))
                self.new_y.append(round(event.ydata))
                self.dstaxes.scatter(self.new_x,self.new_y, s = 40, c = 'Lime')
                plt.draw()
                if event.button != 1:
                    self.dst.append(np.transpose(np.vstack([np.array(self.new_x),np.array(self.new_y)])))
    def gethooks(self):
        return Hooks(self.src[0],self.dst[0])



## some helpful functions ----------------------------------------  

## Fancyer plots
def makeRGBA(M,R = 255, G = 255, B = 255, Thr = 0.0):
''' Convert a 2D mp.array M in a 4 dim RGBA np.array'''
    RGBA = np.zeros([M.shape[0],M.shape[1],4]) ## the empty RGBA cube
    idvisible = M > Thr
    RGBA[idvisible,3] = 1.0
    RGBA[:,:,0] = ((M/np.max(M))*R)/255 ## red
    RGBA[:,:,1] = ((M/np.max(M))*G)/255 ## green
    RGBA[:,:,2] = ((M/np.max(M))*B)/255 ## blue
    return(RGBA)









# # class rois:
# #     def __init__(self,fig,image):
# #         self.ax = fig.gca()    ## returns the active axis instance
# #         self.rois = []
# #         self.ys = []
# #         self.xs = []
# #         self.masks = []
# #         self.intensities= []
# #         self.image = image     ## stores the image used to get the rois
# #     def event_method(self, event):
# #         ## want to pick points only if nothing is selected in the toolbar ...
# #         toolbar = plt.get_current_fig_manager().toolbar  
# #         if toolbar.mode =='':
# #             self.ys.append(round(event.ydata))
# #             self.xs.append(round(event.xdata))
# #             self.ax.scatter(self.xs,self.ys, s = 30, c = 'Lime')
# #             plt.draw()
# #             if event.button != 1:
# #                 self.rois.append(np.vstack([np.array(self.xs),np.array(self.ys)]))
# #                 self.ys = []
# #                 self.xs = []
# #     def getMasks(self):
# #         from skimage.draw import polygon
# #         for roi in self.rois:
# #             empty = np.zeros(self.image.shape, dtype=np.uint8)
# #             rr,cc = polygon(roi[1,:],roi[0,:])
# #             empty[rr, cc] = 1 
# #             self.masks.append(empty)
# #     def getIntensities(self, Ithr = 1000):
# #         from skimage.draw import polygon
# #         for roi in self.rois:
# #             rr,cc = polygon(roi[1,:],roi[0,:])
# #             values = self.image[rr,cc]
# #             self.intensities.append(values[values > Ithr])
# #     def project (self, image, affine = None, Ithr = 1000):
# #         from skimage.draw import polygon
# #         from skimage import transform as tf
# #         ## se no trasformazione applica, se trasformazione trasforma e applica
# #         for roi in self.rois:
# #             rr,cc = polygon(roi[1,:],roi[0,:])
# #             values = image[rr,cc]
# #             return values[values > Ithr]


# class Hooks:
#     def __init__(self,srcaxes,dstaxes):
#         self.srcaxes = srcaxes
#         self.dstaxes = dstaxes
#         self.old_x = []
#         self.old_y = []
#         self.new_x = []
#         self.new_y = []
#         self.sub = []
#         self.src = []
#         self.dst = []
#     def over_method(self,event):
#         self.sub = event.inaxes
#     def click_method(self, event):
#         ## want to pick points only if nothing is selected in the toolbar ...
#         toolbar = plt.get_current_fig_manager().toolbar  
#         if toolbar.mode =='':
#             if self.sub == self.srcaxes:
#                 self.old_x.append(round(event.xdata))
#                 self.old_y.append(round(event.ydata))
#                 self.srcaxes.scatter(self.old_x,self.old_y, s = 40, c = 'Lime')
#                 plt.draw()
#                 if event.button != 1:
#                     self.src.append(np.transpose(np.vstack([np.array(self.old_x),np.array(self.old_y)])))
#             if self.sub == self.dstaxes:
#                 self.new_x.append(round(event.xdata))
#                 self.new_y.append(round(event.ydata))
#                 self.dstaxes.scatter(self.new_x,self.new_y, s = 40, c = 'Lime')
#                 plt.draw()
#                 if event.button != 1:
#                     self.dst.append(np.transpose(np.vstack([np.array(self.new_x),np.array(self.new_y)])))
#     def gethooks(self):
#         ''' Extract the matching points (src to dst) '''
#         return self.src, self.dst


