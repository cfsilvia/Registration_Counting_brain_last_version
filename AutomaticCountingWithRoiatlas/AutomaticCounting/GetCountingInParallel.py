# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 11:48:06 2024

@author: Administrator
"""

import subprocess
import os
from multiprocessing import Pool,cpu_count


def run_imagej_macro(macro_path,inputData):
     #command = f'C:/Fiji.app/ImageJ-win64 --ij2 --headless -macro {macro_path} name1 ={name1}'
     #print(inputData)
     command = ["C:/Fiji.app/ImageJ-win64","--ij2" ,"-Xmx2g","--console","-macro", macro_path, inputData, ]
     subprocess.run(command, shell=True)
     




def GetCounting(Total_inputs,Type_of_stain):
    macros_and_parameters = list()
    # path of the macro
    #if Type_of_stain == "Cfos":
     #   path = 'X:/Users/LabSoftware/ImageJSoftware/AutomaticCountingWithRoiatlas/AutomaticCounting/Counting_Cells_per_slice_Cfos.ijm'
    #else:
    path = 'X:/Users/LabSoftware/ImageJSoftware/AutomaticCountingWithRoiatlas/AutomaticCounting/Counting_Cells_per_slice.ijm'
    #inputs
    for s in Total_inputs:
        macro_info = (path,s)
        macros_and_parameters.append(macro_info)
    
   
      # Run ImageJ macros in parallel
    try:
        num_cores = cpu_count()
        with Pool(processes=num_cores) as pool:
             pool.starmap(run_imagej_macro, macros_and_parameters)
        print("The counting finished")
    finally:
        # Close the Pool to release resources
        pool.close()
        # Wait for all worker processes to finish
        pool.join()