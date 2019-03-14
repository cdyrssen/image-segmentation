import numpy as np
import pylab as py
import useful_functions as uf
from scipy import ndimage
import os
import sys

thresh_mult = 1.00
exp_degree = 3.00
filter_mult = 0.50

fname = str(os.path.basename(__file__))
script_path = str(os.path.realpath(__file__))[:-len(fname)]
root_path = script_path+'data\\'
data_path = root_path+'raw_cropped\\'
img_path = root_path+'exponential_binarized\\'

arguments = sys.argv

data_path = script_path
img_path = script_path

if '-h' in arguments or '--help' in arguments:
    print('-s or --source sets source directory for data')
    print('-d or --destination sets destination directory for segmented images')
    print('-fs or --filter-size sets filter size for denoising. Generally should be value from 0.0 to 1.0.')
    print('-e or --exponent sets the exponent to raise the image to. Generally should be a value from 1.0 to 15.0.')
    print('-t or --threshold sets the threshold value. Generally should be a value from -1.0 to 1.0.')
    print('Argument values are not strictly enforced to be within the above suggested ranges.')
    print('Default values for source and destination directories are the same directory as the python script.')
    print('Default values for the filter size, exponent, and threshold are 0.5, 2.0, and 0.0 respectively.')
    print('In general a larger filter size will remove more noise.')
    print('In general a larger exponent will remove more noise.')
    print('In general a larger threshold will remove more noise.')
    sys.exit()

if '-d' in arguments:
    img_path = arguments[arguments.index('-d')+1]+'\\'
if '--destination' in arguments:
    img_path = arguments[arguments.index('--destination')+1]+'\\'

if '-s' in arguments:
    data_path = arguments[arguments.index('-s')+1]+'\\'
if '--source' in arguments:
    data_path = arguments[arguments.index('--source')+1]+'\\'
    
if '-fs' in arguments:
    try:
        filter_mult = float(arguments[arguments.index('-fs')+1])
    except:
        print('Filter size argument not a float')
        sys.exit()
if '--filter-size' in arguments:
    try:
        filter_mult = float(arguments[arguments.index('-fs')+1])
    except:
        print('Filter size argument not a float')
        sys.exit()
        
if '-e' in arguments:
    try:
        exp_degree = float(arguments[arguments.index('-e')+1])
    except:
        print('Exponent argument not a float')
        sys.exit()
if '--exponent' in arguments:
    try:
        exp_degree = float(arguments[arguments.index('--exponent')+1])
    except:
        print('Exponent argument not a float')
        sys.exit()
        
if '-t' in arguments:
    try:
        thresh_mult = float(arguments[arguments.index('-t')+1])
    except:
        print('Threshold argument not a float')
        sys.exit()
if '--threshold' in arguments:
    try:
        thresh_mult = float(arguments[arguments.index('--threshold')+1])
    except:
        print('Threshold argument not a float')
        sys.exit()

def denoise(img):
    width = image.shape[1]
    height = image.shape[0]
    
    noise_img = uf.convert_to_img(ndimage.laplace(img))
    hist = uf.hist(noise_img)
    std = np.std(noise_img)
    
    noise = std*(height*width)/hist.max()
    filter_size = int(np.sqrt(noise)*filter_mult)
    
    filtered_img = img
    if filter_size > 0:
        filtered_img = ndimage.maximum_filter(filtered_img, filter_size/2)
        filtered_img = ndimage.median_filter(filtered_img, filter_size)
    return filtered_img

files = uf.get_files(data_path)
cnt = 0
for data_file in files:
    image = uf.convert_to_img(uf.get_data(data_file))
    print(cnt)
    filtered_image = image.astype(float)
    filtered_image = denoise(filtered_image)
    filtered_image = np.log(filtered_image)
    filtered_image = filtered_image**exp_degree
    filtered_image[-np.inf == filtered_image] = np.nan
    filtered_image[np.inf == filtered_image] = np.nan
    nan_mean = np.nanmean(filtered_image)
    nan_std = np.nanstd(filtered_image)
    filtered_image[filtered_image < nan_mean+thresh_mult*nan_std] = np.nan
    
    #py.imshow(filtered_image, cmap='gray')
    #py.show()
    
    filtered_image[np.isnan(filtered_image)] = 0
    filtered_image[filtered_image > 0] = 1
    image *= filtered_image.astype(int)
    image = image.astype(float)
    image[image == 0] = np.nan
    py.imsave(img_path+'exponential%02d.png'%cnt, image, cmap='gray')
    cnt += 1    