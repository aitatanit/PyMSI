import numpy as np
import argparse
import cv2

def Shapefactorfeatures(mask):
    Shapefactor = []
    mask = mask
    contours,_ = cv2.findContours(np.uint8(mask),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    lstn = [len(s) for s in contours]
    cnt = contours[lstn.index(max(lstn))]
    M = cv2.moments(cnt)
    x,y,w,h = cv2.boundingRect(cnt)
    Shapefactor.append(float(w)/h)                                          ## aspect ratio
    area = cv2.contourArea(cnt); perimeter = cv2.arcLength(cnt,True)
    Shapefactor.append(area)                                                ## area
    Shapefactor.append(perimeter)                                           ## perimeter
    Shapefactor.append(((4*np.pi*area)/(perimeter**2)))                     ## circularity
    Shapefactor.append(np.sqrt(M['m02']/M['m01']))                          ## elongation factor                     
    return(np.array(Shapefactor))

def main():    
    parser = argparse.ArgumentParser(description="Tissue histology based features calculation")
    parser.add_argument('-f',dest = "filename",required=True, help="input file contains binary/mask image",metavar="FILE")
    args = parser.parse_args()
    Img = np.genfromtxt(args.filename,dtype=float,delimiter=',')
    result = np.zeros([5,1])
    result[:,0] = Shapefactorfeatures(Img)
    column= np.array(['Aspect ratio','Area','perimeter','Circularity','Elongation Factor'])
    df = np.column_stack((column,result))
    np.savetxt('Shapebased_featuresList.csv',df,fmt="%s",delimiter=",")
        
if __name__ == '__main__':
   main()
