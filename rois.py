## Objective:  a function which over an image identifies
## a list of region of interest


import pylab as plt
import matplotlib
from matplotlib.patches import Polygon
import numpy as np
from skimage.draw import polygon

def ROI(matrix):
	'''Interactively identify a list of region of interest 

	The function return a list of binary masks identifying a set of
	region of interest (ROI) over an image represented by a 2D matrix
	The selection of the ROI vertices is done with the left mouse button
	Each ROI is created and stored by pressing 'r' key.


	Args:
	matrix : a 2D Numpy array 

	Returns:
	a list of 2D Numpy masks corresponding to the ROIS
	'''
	class RoiCreator:
	    def __init__(self,fig):
	        ''' Handles the events to create interactively the regions of interset. '''
	        self.ax = fig.gca()    ## returns the active axis instance
	        self.ys = []
	        self.xs = []
	        self.rois = []
	    def event_method(self, event):
	        ''' Event handler for the interactively creation of the region of interest '''
	        ## want to pick points only if nothing is selected in the toolbar ...
	        toolbar = plt.get_current_fig_manager().toolbar 
	        ## keep on plotting the identified rois in re
	        #self.ax.scatter(roi[0],roi[1], s = 30, c = 'red') 
	        if toolbar.mode =='':
	        	if event.button == 1:
	        		self.ys.append(round(event.ydata))
	        		self.xs.append(round(event.xdata))
	            	self.ax.scatter(self.xs,self.ys, s = 30, c = 'Lime')
	            	plt.draw()              
	    def event_method_key(self,event):
	    	''' Store the roi data on key pressing'''
	    	toolbar = plt.get_current_fig_manager().toolbar
	    	if toolbar.mode =='':
	    		self.rois.append(np.vstack([np.array(self.xs),np.array(self.ys)]))
	    		mycoord = np.array([self.xs,self.ys]).transpose()
	    		pol = Polygon(mycoord, color = 'Red', alpha = 0.6)
	    		self.ys = []
	    		self.xs = []
	    		self.ax.add_patch(pol)
	## create and show the figure 
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_title('ROI selection')
	ax.imshow(matrix, interpolation = 'None')
	## get the regions of interests
	tmprois = RoiCreator(fig)
	cid = fig.canvas.mpl_connect('button_press_event', tmprois.event_method)
	pid = fig.canvas.mpl_connect('key_press_event', tmprois.event_method_key)
	plt.show()
	masks = []
	for roi in tmprois.rois:
		empty = np.zeros(matrix.shape, dtype=np.uint8)
		rr,cc = polygon(roi[1,:],roi[0,:])
		empty[rr, cc] = 1
		masks.append(empty)
	return(masks)
