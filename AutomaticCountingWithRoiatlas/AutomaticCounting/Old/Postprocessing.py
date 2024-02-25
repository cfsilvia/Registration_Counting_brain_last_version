# -*- coding: utf-8 -*-

'''
Processing all the csv files 
'''

from pandas.io.excel import ExcelWriter
import pandas as pd
import os
from glob  import glob

def Postprocessing(Folder_with_data, Type_of_stain,separation):
    #all the csv  files
    files = sorted(glob(Folder_with_data + 'CountingResultOf' + Type_of_stain + '/' + '*.xls'))
    #create data frame with all the data
    Table_with_all_data = Join_csv_data(files)
    #find unique regions
    unique_sectors = pd.unique(Table_with_all_data['Region considered'])
    Table_with_all_data = AddData(Table_with_all_data)
    # go through each region 
    SaveSector(Folder_with_data,Table_with_all_data,unique_sectors,separation)
    a=1

    
    
def Join_csv_data(files):
    frames = []
    for f in files:
        df = pd.read_table(f)
        frames.append(df)
        
    result = pd.concat(frames)
    return result

def SaveSector(Folder_with_data, Table_with_all_data,unique_sectors,separation):
    output = Folder_with_data + 'TotalDataVs1.xlsx'
    with pd.ExcelWriter(output) as writer:
      for s in unique_sectors:
        data = Table_with_all_data[Table_with_all_data['Region considered'] == s]
        data['Number Slice'] = GetNumberSlice(data,separation)
        data = Sort_slice(data)
        index = s.find('/')
        if(index != -1):
            s =s.replace("/","_")
        data.to_excel(writer, sheet_name = s, index = False)
        print(s)
      print("Number of regions",len(unique_sectors))  

        
        
def Sort_slice(data):
    data.sort_values(by =['Number Slice'], inplace=True)
    return data
    

def GetNumberSlice(data,separation):
    aux = data['Brain slice']
    list_slice =[]
    for row in aux:
        new = int(row.split(separation)[0])
        list_slice.append(new)
    
    return list_slice

def AddData(data):
    data.insert(4,"Total Density 1/mm^2", data["Number of Labels"]/data["Area of all the ROI mmxmm"])
    data.insert(7,"Density Left 1/mm^2", data["Number of Labels Left"]/data["Area of Left ROI mmxmm"])
    data.insert(10,"Density Right 1/mm^2", data["Number of Labels Right"]/data["Area of Right ROI mmxmm"])
    return data 