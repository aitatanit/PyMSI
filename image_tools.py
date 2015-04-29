
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






## some helpful functions ----------------------------------------  

## Fancyer plots







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


