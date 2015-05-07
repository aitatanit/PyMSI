## This file contains function to calculate Haralick texture features 
## Args : 2D co-occurrence matrix 

import cmath
import pandas
import numpy as np

def _entropy(p):
    p = p.ravel()
    return -np.dot(np.log2(p+(p==0)),p)

def gray_features(p):
    feats = np.zeros(13,np.double)
    maxv = len(p)
    k = np.arange(maxv)
    k2 = k**2
    tk = np.arange(2*maxv)
    tk2 = tk**2
    i,j = np.mgrid[:maxv,:maxv]
    ij = i*j
    i_j2_p1 = (i - j)**2
    i_j2_p1 += 1
    i_j2_p1 = 1. / i_j2_p1
    i_j2_p1 = i_j2_p1.ravel()
    px_plus_y = np.empty(2*maxv, np.double)
    px_minus_y = np.empty(maxv, np.double)
    pravel = p.ravel()
    px = p.sum(0)
    py = p.sum(1)
    ux = np.dot(px, k)
    uy = np.dot(py, k)
    vx = np.dot(px, k2) - ux**2
    vy = np.dot(py, k2) - uy**2
    sx = np.sqrt(vx)
    sy = np.sqrt(vy)
    px_plus_y = np.zeros(shape=(2*p.shape[0] ))
    px_minus_y = np.zeros(shape=(p.shape[0]))
    for i in range(p.shape[0]):
       for j in range(p.shape[0]):
           p_ij = p[i,j]
           px_plus_y[i+j] += p_ij
           px_minus_y[np.abs(i-j)] += p_ij
    feats[0] = np.sqrt(np.dot(pravel, pravel))                                 # Energy
    feats[1] = np.dot(k2, px_minus_y)                                 # Contrast
    if sx == 0. or sy == 0.:
       feats[2] = 1.
    else:
       feats[2] = (1. / sx / sy) * (np.dot(ij.ravel(), pravel) - ux * uy) # Correlation
    feats[3] = vx                                                     #Sum of Squares: Variance     
    feats[4] = np.dot(i_j2_p1, pravel)                                # Inverse of Difference Moment
    feats[5] = np.dot(tk, px_plus_y)                                  # Sum Average
    feats[7] = _entropy(px_plus_y)                                    # Sum Entropy
    feats[6] = ((tk-feats[7])**2*px_plus_y).sum()                     # Sum Variance
    feats[8] = _entropy(pravel)                                       # Entropy
    feats[9] = px_minus_y.var()                                       # Difference Variance
    feats[10] = _entropy(px_minus_y)                                  # Difference Entropy
    HX = _entropy(px)
    HY = _entropy(py)
    crosspxpy = np.outer(px,py)
    crosspxpy += (crosspxpy == 0) 
    crosspxpy = crosspxpy.ravel()
    HXY1 = -np.dot(pravel, np.log2(crosspxpy))
    HXY2 = _entropy(crosspxpy)
    if max(HX, HY) == 0.:
       feats[11] = (feats[8]-HXY1)                                    # Information Measure of Correlation 1                    
    else:
       feats[11] = (feats[8]-HXY1)/max(HX,HY)
    feats[12] = np.sqrt(max(0,1 - np.exp( -2. * (HXY2 - feats[8]))))  # Information Measure of Correlation 2
    return feats

