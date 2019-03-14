# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 21:45:40 2018

@author: Toffer
"""

from matplotlib import pyplot as plt
from scipy import ndimage
from  skimage import exposure
import useful_functions as uf
import numpy as np
import os

script_name = str(os.path.basename(__file__))
root_path = str(os.path.realpath(__file__))[:-len(script_name)]
raw_data_path = root_path+'data\\raw\\'
raw_img_path = root_path+'data\\raw_img\\'
raw_cropped_path = root_path+'data\\raw_cropped\\'
first_filter = root_path+'data\\first_threshold\\'
second_filter = root_path+'data\\second_threshold\\'
cropped_path = root_path+'data\\cropped\\'
log_path = root_path+'data\\log\\'
files = uf.get_files(raw_data_path)

log_degree = 0.25

cnt = 0
for data_file in files:
    print cnt

    data = uf.get_data(data_file)
    plt.imsave(raw_img_path+'raw_img%02d.png'%cnt, data, cmap='gray')
    
    blurred = ndimage.gaussian_filter(data, 100)
    blurred = uf.threshold(uf.convert_to_img(blurred), 145)
    
    plt.imshow(blurred, cmap='gray')
    plt.imsave(first_filter+'first_thresh%02d.png'%cnt, blurred, cmap='gray')
    
    hMinIndex = blurred.shape[1]
    hMaxIndex = 0
    for row in blurred:
        for pixel in range(len(row)):
            if row[pixel] != 0:
                hMinIndex = pixel if hMinIndex > pixel else hMinIndex
                break
        row = np.flip(row, axis=0)
        tmp = blurred.shape[1]
        for pixel in range(len(row)):
            if row[pixel] != 0:
                hMaxIndex = tmp-pixel if hMaxIndex < tmp-pixel else hMaxIndex
                
    if hMinIndex-30 > 0:
        hMinIndex -= 30
    else:
        hMinIndex = 0
    if hMaxIndex+30 < blurred.shape[1]:
        hMaxIndex += 30
    else:
        hMaxIndex = blurred.shape[1]
    img_data = uf.convert_to_img(data[:,hMinIndex:hMaxIndex])

    #plt.imsave(cropped_path+'first_crop%d.png'%count, img_data cmap='gray')

    shape = img_data.shape
    
    med = ndimage.median_filter(img_data, 5)
    blurred = ndimage.gaussian_filter(med, 3)
    blurred = uf.threshold(uf.convert_to_img(blurred), 35)
    
    plt.imshow(blurred, cmap='gray')
    plt.imsave(second_filter+'second_thresh%02d.png'%cnt, blurred, cmap='gray')
    
    vMinIndex = blurred.shape[0]
    vMaxIndex = 0
    for row in blurred.transpose():
        for pixel in range(len(row)):
            if row[pixel] != 0:
                vMinIndex = pixel if vMinIndex > pixel else vMinIndex
                break
        row = np.flip(row, axis=0)
        tmp = blurred.shape[0]
        for pixel in range(len(row)):
            if row[pixel] != 0:
                vMaxIndex = tmp-pixel if vMaxIndex < tmp-pixel else vMaxIndex

    
    vMinIndex -= 30 if vMinIndex-30 > 0 else 0
    vMaxIndex += 30 if vMaxIndex+30 < blurred.shape[1] else blurred.shape[1]
    
    img_data = uf.convert_to_img(data[vMinIndex:vMaxIndex,hMinIndex:hMaxIndex])
    plt.imsave(cropped_path+'crop%02d.png'%cnt, img_data, cmap='gray')
    plt.close()
    
    log_data = uf.convert_to_img(exposure.adjust_log(img_data, log_degree))
    plt.imsave(log_path+'log%02d.png'%cnt, log_data, cmap='gray')
    plt.close()
    
    raw_data = uf.get_data_raw(data_file)
    raw_data = raw_data[vMinIndex:vMaxIndex,hMinIndex:hMaxIndex]
    with open(raw_cropped_path+'raw_cropped%02d.asc'%cnt, 'w') as raw_crop:
        line_num = 1
        for line in raw_data:
            raw_crop.write(str(line_num)+'\t')
            for pixel in line:
                raw_crop.write(str(int(pixel))+'\t')
            raw_crop.write('\n')
            line_num += 1
    
    cnt += 1