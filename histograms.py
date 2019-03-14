
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 01 16:29:12 2018

@author: Toffer
"""

import histogram_generator as hg

hg.generate_histograms('cropped', ext='.png', bins=128)
hg.generate_histograms('log', ext='.png', bins=128)
hg.generate_histograms('raw')
hg.generate_histograms('raw_cropped')