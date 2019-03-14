# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 02:14:42 2018

@author: Toffer
"""

from matplotlib import pyplot as plt
from scipy import ndimage
from scipy.signal import wiener
from skimage import exposure
import useful_functions as uf
import numpy as np
import os

def denoise(img, size=7):
    tmp = wiener(img, size)
    return tmp

#def laplace_denoise(img):
    

script_name = str(os.path.basename(__file__))
root_path = str(os.path.realpath(__file__)[:-len(script_name)])
crop_path = root_path+'data\\cropped\\'
laplace_path = root_path+'data\\laplace\\'
filtered_path = root_path+'data\\laplace_filtered\\'
binarized_path = root_path+'data\\laplace_binarized\\'
files = uf.get_files(crop_path, ext='.png')

# parameters
mean_multiplier = 45 # can be 1-25
rank_filter_size = 4 # can be 1-5
rank_filter_rank = 5 # can be 0-rank_filter_size+1

cnt = 0
for data_file in files:
    print cnt
    img = uf.convert_to_img(uf.get_data(data_file))
    img = uf.convert_to_img(denoise(img))
    img = ndimage.maximum_filter(img, 3)
    
    img = denoise(img)
    laplace_img = uf.convert_to_img(ndimage.gaussian_laplace(img,1))
    plt.imsave(laplace_path+'laplace%02d'%cnt, 
                uf.convert_to_img(laplace_img), 
                cmap='gray')
    
    laplace_img = denoise(laplace_img)
    laplace_img = uf.convert_to_img(laplace_img)
    plt.imsave(filtered_path+'filtered%02d.png'%cnt, 
               uf.convert_to_img(laplace_img),
               cmap='gray')

    hist = uf.hist(laplace_img)
    
    # range from hist mean to 10*hist mean
    updated_hist = np.zeros_like(hist)
    for i in range(len(hist)):
        if hist[i] < np.mean(hist)*mean_multiplier:
            updated_hist[i] = 1
        else:
            break
    rev_hist = np.flip(hist, axis=0)
    for i in range(len(hist)-1, 0, -1):
        if hist[i] < np.mean(hist)*mean_multiplier:
            updated_hist[i] = 1
        else:
            break
    
    laplace_thresh = uf.convert_to_img(laplace_img)
    for x in range(laplace_thresh.shape[0]):
        for y in range(laplace_thresh.shape[1]):
            if updated_hist[laplace_thresh[x, y]] == 1:
                laplace_thresh[x, y] = 255
            else:
                laplace_thresh[x, y] =  0
        
    plt.imsave(binarized_path+'lapl_bin%02d'%cnt, laplace_thresh, cmap='gray')
    cnt +=  1