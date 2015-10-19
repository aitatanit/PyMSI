#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import argparse
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
import pandas.rpy.common as com
from pandas import DataFrame

def Sizezonematrixfeatures(Img):
    rdf = com.convert_to_r_dataframe(Img)
    ro.globalenv['Image'] = rdf
    ro.r('Image <- as.matrix(Image)')
    ro.r('library(radiomics)')
    ro.r('szmatrix <- glszm(Image)')
   # ro.r('szmatrix[nrow(szmatrix),] <- 0')
    ro.r('szmfeature <- array(NA,dim=c(11,1))')
    ro.r('szmfeature[1,1] <- glszm_SAE(szmatrix)')
    ro.r('szmfeature[2,1] <- glszm_LAE(szmatrix)')
    ro.r('szmfeature[3,1] <- glszm_IV(szmatrix)')
    ro.r('szmfeature[4,1] <- glszm_HILAE(szmatrix)')
    ro.r('szmfeature[5,1] <- glszm_LILAE(szmatrix)')
    ro.r('szmfeature[6,1] <- glszm_HISAE(szmatrix)')
    ro.r('szmfeature[7,1] <- glszm_LISAE(szmatrix)')
    ro.r('szmfeature[8,1] <- glszm_HIE(szmatrix)')
    ro.r('szmfeature[9,1] <- glszm_LIE(szmatrix)')
    ro.r('szmfeature[10,1] <- glszm_ZP(szmatrix)')
    ro.r('szmfeature[11,1] <- glszm_SZV(szmatrix)')
    ro.r('colname <-c("SAE","LAE","IV","SZV","ZP","LIE","HIE","LISAE","HISAE","LILAE","HILAE")')
    ro.r('szmfeat <- cbind(colname,szmfeature)')
    ro.r('write.csv(szmfeat,file="SZM_featuresList.csv")')

def main():    
    parser = argparse.ArgumentParser(description="Size-zone matrix based features calculation")
    parser.add_argument('-f',dest = "filename",required=True, help="input file with image matrix",metavar="FILE")
    args = parser.parse_args()
    Img = np.genfromtxt(args.filename,dtype= float,delimiter=',')
    Img = DataFrame(Img)
    Sizezonematrixfeatures(Img)

        
if __name__ == '__main__':
   main()
