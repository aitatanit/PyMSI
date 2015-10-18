'''
Command to run script : 
~/Documents/MSimaging$ python Features_Firstorderstatistics.py -f '~/Documents/MSimaging/Images/A1.csv'

'''

import numpy as np
from scipy import stats
import argparse

def Firstorderstatistics(Imgarray):
    '''Function calculate first order statistics for tissue object'''
    FOS = []
    graylevelarray = Imgarray
    FOS.append(len(graylevelarray))            # pixel count
    FOS.append(np.sum(graylevelarray))         # intensity sum within tissue
    FOS.append(np.mean(graylevelarray))        # intensity mean within tissue
    FOS.append(np.std(graylevelarray))         # standard deviation
    FOS.append(np.var(graylevelarray))         # variance
    FOS.append(stats.kurtosis(graylevelarray)) # kurtosis
    FOS.append(stats.skew(graylevelarray))     # skewness
    return(np.array(FOS))

def main():    
    parser = argparse.ArgumentParser(description="First order statistics based features calculation")
    parser.add_argument('-f',dest = "filename",required=True, help="input file with image matrix",metavar="FILE")
    args = parser.parse_args()
    Img = np.genfromtxt(args.filename,dtype=float,delimiter=',')
    Img = Img.flatten()
    Img_new = Img[Img<np.max(Img)]
    result = np.zeros([7,1])
    result[:,0] = Firstorderstatistics(Img_new)
    column= np.array(['Nu of pixles','Intensity sum','Intensity mean','Std deviation','variance','kurtosis','skewness'])
    df = np.column_stack((column,result))
    np.savetxt('FOS_featuresList.csv',df,fmt="%s",delimiter=",")
        
if __name__ == '__main__':
   main()
