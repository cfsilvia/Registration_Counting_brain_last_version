# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 11:20:11 2024

@author: Administrator
"""

# Filter data
import matplotlib.pyplot as plt
from stardist.plot import render_label
from skimage import io, measure
import numpy as np
import statistics
import concurrent.futures
from skimage.measure import regionprops

def FilterData(labels, img,details):
    min_area = 120 #120
    max_area = 900 #1000
    
    # Use the label function to obtain label data
  #  label_data = measure.label(labels)
    
    # Use regionprops to get properties of each labeled region
    regions = measure.regionprops(labels)
    r = regionprops(labels,img)
    # Filter objects based on area
    filtered_objects = []
    index_objects =[]
    intensity_objects = []
    index=0
    for props in r:
        intensity_values =np.mean(img[props.coords[:, 0], props.coords[:, 1]])
        intensity_objects.append(intensity_values)
    
 
        
        
        
        
    lower_value = 10*(min(intensity_objects))
    #%%
    #filter according area and intensity
    for prop in regions:
       if min_area <= prop.area <= max_area:
           
        if intensity_objects[index] > lower_value:
          filtered_objects.append(prop)
          index_objects.append(index)
       index+=1
    
    
    new_details = details['coord']
    new_details = new_details[index_objects]
    
    return new_details



##Define parallel function
# Define the function to be executed in parallel
def parallel_function(index, regions, min_area, max_area,img, labels):
    if min_area <= regions[index].area <= max_area:
      # Extract intensity values from original image for the labeled region
      label_intensity_values = img[labels == regions[index].label]

      # Calculate mean intensity value for the labeled region
      result = np.mean(label_intensity_values)
    else:
      result = 0 #not considered
      
    return result