# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 20:39:59 2018

@author: Toffer
"""
import os
import useful_functions as uf
from matplotlib import pyplot as plt
from scipy.signal import savgol_filter

def generate_histograms(path='raw', bins=256, ext='.asc'):
    path += '\\'
    fname = str(os.path.basename(__file__))
    script_path = str(os.path.realpath(__file__))[:-len(fname)]
    root_path = script_path+'data\\'
    img_path = root_path+path
    hist_path = root_path+path[:-1]+'_hist\\'
    files = uf.get_files(img_path, ext)
    
    cnt = 0
    for data_file in files:
        print cnt
        data = uf.get_data(data_file)
        
        hist = uf.hist(data, bins=bins)
        #hist = savgol_filter(hist, 5, 3)
        #hist = fft(hist)
        
        plt.plot(hist)
        plt.savefig(hist_path+path[:-1]+'_hist%02d.png'%cnt)
        plt.close()
        
        #print np.amax(hist), np.median(hist), np.mean(hist), hist.std()
        cnt += 1