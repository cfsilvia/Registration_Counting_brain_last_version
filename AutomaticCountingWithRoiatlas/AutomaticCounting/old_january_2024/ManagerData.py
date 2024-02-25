# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 10:16:43 2023

@author: Administrator
Manager data
"""
from glob  import glob
from tifffile import imread
from stardist import export_imagej_rois
from Stardist_prediction import Stardist_prediction
from GetCounting import GetCounting
import os
import imagej

from stardist import fill_label_holes, random_label_cmap, calculate_extents, gputools_available
from stardist import random_label_cmap, _draw_polygons, export_imagej_rois
from stardist.models import Config2D, StarDist2D, StarDistData2D

'''
ManagerData the function loop through each slice find all the labels and then counts the labels
of each region
input: folder with data which includes folder ROI_From_Atlas and also folder with the pictures
output: one folder with csv for each slice with counting. and one folder with the marking of the labels
'''

def ManagerData(Folder_with_data, Type_of_stain,scale):
    #%%
    ij = imagej.init(r'C:/Fiji.app', headless=False)
    #load stardist model
    model = Stardist_model(Type_of_stain)
    #list the images files in the folder/read the images
    X_file = sorted(glob(Folder_with_data + Type_of_stain + '/' +'*.tif'))
    X = list(map(imread,X_file))
    #%% Applied stardist to each image after normalization
    for index in range(len(X)):
        #%%
         labels,details = Stardist_prediction(model, X[index])
       
         print(X_file[index])
        # #%% save the labels
         path =  Folder_with_data + 'Roi_all_image/'
         Create_folder(path)
        # # file name with extension
         file_name = os.path.basename(X_file[index])
        # # file name without extension
         filename = os.path.splitext(file_name)[0]
        # #%Export rois to imagej
         export_imagej_rois(path + filename +'.zip', details['coord'])
        #%%Get through image j countings of labels inside roi of atlas
         GetCounting(Folder_with_data, Type_of_stain,filename,ij,scale)
       
           
           
           
def Create_folder(path):
    isExist = os.path.exists(path)
    if not isExist:
       # Create a new directory because it does not exist
       os.makedirs(path)
       
def Stardist_model(Type_of_stain):
    #%%
    # 32 is a good default choice (see 1_data.ipynb)
    n_rays = 128

    # Use OpenCL-based computations for data generator during training (requires 'gputools')
    use_gpu = False and gputools_available()

    # Predict on subsampled grid for increased efficiency and larger field of view
    grid = (2,2)
    n_channel = 1
    conf = Config2D (
        n_rays       = n_rays,
        grid         = grid,
        use_gpu      = True,
        n_channel_in = n_channel,
    )
    print(conf)
    vars(conf)
    
    #%%Load train model
    if Type_of_stain == "P16":
       directory_model = 'X:/Users/LabSoftware/ImageJSoftware/AutomaticCounting/P16virus_model/models'
       model = StarDist2D(None, name='stardist_test', basedir= directory_model)
    elif Type_of_stain == "Cfos":
        # creates a pretrained model
       model = StarDist2D.from_pretrained('2D_versatile_fluo')
    return model