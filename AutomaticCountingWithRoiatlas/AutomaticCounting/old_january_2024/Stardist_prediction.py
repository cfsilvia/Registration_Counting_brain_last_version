# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 10:54:53 2023

@author: Administrator
Stardist prediction for one image

"""

from csbdeep.utils import Path, normalize
from csbdeep.io import save_tiff_imagej_compatible

from stardist import fill_label_holes, random_label_cmap, calculate_extents, gputools_available
from stardist import random_label_cmap, _draw_polygons, export_imagej_rois
from stardist.models import Config2D, StarDist2D, StarDistData2D



#%%
def Stardist_prediction(model,image):
    axis_norm = (0,1)# normalize channels independently

    img = normalize(image, 1,99.8, axis=axis_norm)
    labels, details = model.predict_instances(img,n_tiles=model._guess_n_tiles(img),show_tile_progress=True)
    n_tiles=model._guess_n_tiles(img)
    print(n_tiles)
    return labels, details