## Objective:  a function which plots the two matrices 
## allows the interactive selection of corresponding points
## and returns a list with source and destination points

import pylab as plt
import numpy as np


def hookthem(srcmatrix,dstmatrix):
    ''' Function to get interactively reference points for affine transformation

    The function displays side by side the plot of the source and destination matrices.
    Use the left mouse button to select corresponding points in the two images. 
    When you are done, store the results with a click of the right button.
    Note: To perform an affine transformation, at least three corresponding points
    should be identified

    Args:
    srcmatrix: source matrix
    dstmatrix: destination matrix
    '''
    ## define the class taking care of the event handling.
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
                    if event.button == 1:
                        self.old_x.append(round(event.xdata))
                        self.old_y.append(round(event.ydata))
                        self.srcaxes.scatter(self.old_x,self.old_y, s = 40, c = 'Lime')
                        plt.draw()
                if self.sub == self.dstaxes:
                    if event.button == 1:
                        self.new_x.append(round(event.xdata))
                        self.new_y.append(round(event.ydata))
                        self.dstaxes.scatter(self.new_x,self.new_y, s = 40, c = 'Lime')
                        plt.draw()
                if event.button !=1:
                    self.src.append(np.transpose(np.vstack([np.array(self.old_x),np.array(self.old_y)])))
                    self.dst.append(np.transpose(np.vstack([np.array(self.new_x),np.array(self.new_y)])))
        def gethooks(self):
            return self.src[0],self.dst[0]
    ## create the figure
    fig = plt.figure()
    inx = fig.add_subplot(1,2,1)
    inx.set_title('Input Image')
    inx.imshow(srcmatrix, interpolation = "None")
    oux = fig.add_subplot(1,2,2)
    oux.set_title('Output Image')
    oux.imshow(dstmatrix, interpolation = "None")
    ## connect the event handlers
    myhooks = HookCreator(inx,oux)
    cid = fig.canvas.mpl_connect('axes_enter_event', myhooks.over_method)
    cid1 = fig.canvas.mpl_connect('button_press_event', myhooks.click_method)
    plt.show()
    return(myhooks.gethooks())

 
