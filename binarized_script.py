# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 19:22:29 2018

@author: Toffer
"""
import os
import useful_functions as uf
import numpy as np
from scipy import ndimage
from scipy.signal import wiener, decimate
from skimage import exposure
from matplotlib import pyplot as plt

def denoise(img):
    tmp = ndimage.minimum_filter(img, 3)
    tmp = wiener(tmp, 2)
    tmp = ndimage.maximum_filter(tmp, 2)
    tmp = ndimage.rank_filter(tmp, 2, 2)
    tmp = ndimage.gaussian_filter(tmp, 0.5)
    return tmp

def denoise_log(img, log=0.25):
    tmp = exposure.adjust_log(img, log)
    tmp = ndimage.minimum_filter(tmp, 3)
    tmp = ndimage.maximum_filter(tmp, 5)
    tmp = ndimage.uniform_filter(tmp, 3)
    tmp = wiener(tmp, 2)
    tmp = ndimage.median_filter(tmp, 3)
    tmp = ndimage.rank_filter(tmp, 1, 2)
    tmp = uf.convert_to_img(tmp)
    return tmp

fname = str(os.path.basename(__file__))
script_path = str(os.path.realpath(__file__))[:-len(fname)]
root_path = script_path+'data\\'
binarized_path = root_path+'binarized\\'
log_path = root_path+'log_binarized\\'
img_path = root_path+'cropped\\'
  
files = uf.get_files(img_path, ext='.png')

# Thresholding parameters
log_degree = 0.25
log_mult = 1.00
std_mult = 0.00

# Decimation parameters
dec_data = False
dec_filter = False
dec_factor = 2

cnt = 0
for data_file in files:
    print cnt
    data = uf.get_data(data_file).astype(int)
    dec_axis = 0 if data.shape[0]>data.shape[1] else 1
    if dec_data:
        data = uf.convert_to_img(decimate(data, dec_factor, axis=dec_axis))
        
    filtered_log = denoise_log(data, log_degree)
    filtered = denoise(data)
    if dec_filter:
        filtered_log = decimate(filtered_log, dec_factor, axis=dec_axis)
        filtered = decimate(filtered, dec_factor, axis=dec_axis)
        
    data_hist = uf.hist(data)
    std_hist = uf.hist(filtered)
    log_hist = uf.hist(filtered_log)
    
    right_index = len(std_hist)-1
    for index in range(right_index, 0, -1):
        if data_hist[index] > np.mean(std_hist)+std_hist.std()*std_mult:
            right_index = index
            break
        
    binarized = uf.threshold(filtered, right_index)
    plt.imsave(binarized_path+'binarized%02d'%cnt, binarized, cmap='gray')
    plt.close()
        
    for index in range(right_index, 0, -1):
        if data_hist[index] > np.mean(log_hist)+log_hist.std()*log_mult:
            right_index = index
            break
    log_binarized = uf.threshold(filtered_log, right_index)
    plt.imsave(log_path+'log_binarized%02d'%cnt, log_binarized, cmap='gray')
    plt.close()

    cnt += 1