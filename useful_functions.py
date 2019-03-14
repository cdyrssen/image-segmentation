# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 22:32:02 2018

@author: Toffer
"""
import os
import glob
import numpy as np
from scipy.misc import imread

def get_files(directory, ext='.asc'):
    # Get all the .asc file names in the specified directory
    directory += '*'+ext
    files = glob.glob(directory)
    return files

def convert_to_img(data):
    # Scale the range of values down to the range of 0-255 to display as image
    maximum = np.amax(data)
    minimum = np.amin(data)
    span = maximum-minimum
    scaled = (data-minimum).astype(float)
    if span != 0:    
        scaled /= float(span)
    else:
        return data
    scaled *= 255
    scaled[np.isnan(scaled)] = 0
    return scaled.astype(int)

def threshold(img, threshold):
    # Create a mask based on the threshold. After the mask has been made, 
    # filter the data and change the value to either 0 or 255.
    mask = img > threshold
    out_img = mask.astype(int)*255
    return out_img

def set_range_start_to_zero(data):
    data -= np.amin(data)
    return data

def get_data(file_name):
    file_name, ext = os.path.splitext(file_name)
    if ext == '.asc':
        with open(file_name+ext, 'r') as fr:
            data = fr.readlines()
            data = np.array([line.strip().split('\t') for line in data])
            data = data.astype(np.float)[:,1:]
    else:
        data = imread(file_name+ext, flatten=True)
        
    return data#set_range_start_to_zero(data)

def get_data_raw(file_name):
    with open(file_name, 'r') as fr:
        data = fr.readlines()
        data = np.array([line.strip().split('\t') for line in data])
        data = data.astype(np.float)[:,1:]
    return data

def image_histogram(img):
    hist = [0]*256
    for i in range(255):
        mask = img == i
        hist[i] = np.sum(mask.flatten())
    return hist.flatten()
    
def translate(data, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = np.amax(data) - np.amin(data)
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = (data - np.amin(data)) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return  (rightMin + (valueScaled * rightSpan)).astype(int)

def hist(data, bins=256):
    hist = np.zeros(bins)
    a = translate(data, 0, bins-1)
    data = convert_to_img(data)
    
    for row in a:
        for pixel_value in row:       
            hist[pixel_value] += 1
            
    hist.flatten()
    return hist

def get_line(start, end):
    
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return np.array(points).astype(int)

def seed_locations(img):
    height = img.shape[0]
    width = img.shape[1]
    p1 = (width-1, 0)
    p2 = (0, height-1)
    horizontal = np.array([(x, y) for x, y in enumerate([height/2]*width)])
    vertical = np.array([(x, y) for y, x in enumerate([width/2]*height)])
    pos_diagonal = get_line((0, 0), (width-1, height-1))
    neg_diagonal = get_line(p1, p2)
    
    seeds = []
    was_white = False
    for pixel in horizontal:
        if not was_white and img[pixel[1], pixel[0]] == 255:
            was_white = True
            seeds.append(pixel)
        elif was_white and img[pixel[1], pixel[0]] == 0:
            was_white = False

    was_white = False
    for pixel in vertical:
        if not was_white and img[pixel[1], pixel[0]] == 255:
            was_white = True
            seeds.append(pixel)
        elif was_white and img[pixel[1], pixel[0]] == 0:
            was_white = False
            
    traversal_axis = 0 if height > width else 1
    was_white = False
    prev_pixel = [-1, -1]
    for pixel in pos_diagonal:
        if not was_white and img[pixel[1], pixel[0]] == 255:
            was_white = True
            seeds.append(pixel)
        elif prev_pixel[traversal_axis] == pixel[traversal_axis]:
            if was_white and img[pixel[1], pixel[0]] == 0:
                was_white = False
        elif img[prev_pixel[1]+1, prev_pixel[0]] == 0 and \
             img[prev_pixel[1], prev_pixel[0]+1] == 0:
                 was_white = False
                 if img[pixel[1], pixel[0]] == 255:
                     seeds.append(pixel)
                     was_white = True
        prev_pixel = pixel

    was_white = False
    prev_pixel = [-1, -1]
    for pixel in neg_diagonal:
        if not was_white and img[pixel[1], pixel[0]] == 255:
            was_white = True
            seeds.append(pixel)
        elif prev_pixel[traversal_axis] == pixel[traversal_axis]:
            if was_white and img[pixel[1], pixel[0]] == 0:
                was_white = False
        elif img[prev_pixel[1]+1, prev_pixel[0]] == 0 and \
             img[prev_pixel[1], prev_pixel[0]+1] == 0:
                 was_white = False
                 if img[pixel[1], pixel[0]] == 255:
                     seeds.append(pixel)
                     was_white = True
        prev_pixel = pixel 
    
    return np.array(seeds)
