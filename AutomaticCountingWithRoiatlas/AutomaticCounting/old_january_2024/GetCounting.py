# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 15:06:07 2023

@author: Administrator
include the macros of imagej
"""
import os
import imagej

def GetCounting(Folder_with_data, Type_of_stain,filename,ij,scale):
    image_input = Folder_with_data + Type_of_stain + '/' + filename + '.tif'
    roi_input = Folder_with_data + 'Roi_all_image/' + filename + '.zip'
    roi_atlas = Folder_with_data + 'ROI_From_Atlas/' + 'RoiSet' + filename +'.zip'
    outputDir =  Folder_with_data + 'CountingResultOf' + Type_of_stain + '/'
    outputImages = Folder_with_data + 'LabeledImagesOf' + Type_of_stain + '/'
    #%% check if the directories were created 
    Create_folder(outputDir)
    Create_folder(outputImages)
    #%%# Create an ImageJ2 gateway with the newest available version of ImageJ2.
    
    # ij = imagej.init(r'C:/Fiji.app', headless=False)
    #%% run macro
    macro = """
#@ String image_input
#@ String roi_input
#@ String roi_atlas
#@ String outputDir
#@ String outputImages
#@ float scale
    ////////////////////////////////////////Function////////////////////

///
    function ArrayIndexWithtSelectionIntersection(r,nR,nTotal ) { //find roi index without intersection of main selection with the stardist detections
     indexdel1=newArray(0);
     for (vr1 = nR; vr1 < (nTotal-1); vr1++) {
       roiManager("select",newArray(r,vr1));
       roiManager("AND"); //find joining
       if (selectionType > -1 ) {
         indexdel1= Array.concat(indexdel1, vr1);
        }
        }
    return indexdel1;
    }
///
function FindSector(nR,Sector){
   for (vr1 = 0; vr1 < nR; vr1++) {
      roiManager("select",vr1);
        rName = Roi.getName(); 
       
      if(rName == Sector){
        index = vr1;
            }
     }
   return index;
}
///
function FindOnSector(arraySelection,indexSector){
    nlabels = 0;
    for(i =0; i<arraySelection.length; i++){
        roiManager("select",newArray(arraySelection[i],parseInt(indexSector)));
        roiManager("AND"); //find joining
       if(selectionType > -1 ){
         nlabels = nlabels + 1;
        }
      }
    return nlabels;
}
///
function FindArea(r,indexSector){
if(r != indexSector){
         roiManager("select",newArray(r,indexSector));
         roiManager("AND"); //find joining
   if(selectionType > -1 ){
       getStatistics(area);
         areaRoi = area/(1000000*1000000);
        } else{
        areaRoi = 0;
       }
   }else {
         roiManager("select", indexSector);
         getStatistics(area);
         areaRoi = area/(1000000*1000000);
}
return areaRoi;
}



/////////////////////////////////////////////////BEGIN PROGRAM//////////////////////////////////////////////////////
    //scale = 648.4;
    scale = scale;
    name_file =substring(image_input, lastIndexOf(image_input, "/")+1, lastIndexOf(image_input, "."));
    //Open the image
    open(image_input);
    run("Set Scale...", "distance=0 known=0 pixel=1 unit=pixel");
    rename("Original");  
    //Open roi
    roiManager("reset");
    roiManager("open",roi_atlas);
    nR = roiManager("Count");  // number of ROI per image.
    print(nR);    
    
    //Find Left /Right
    indexLeft = FindSector(nR,"Left"); 
    indexRight = FindSector(nR,"Right"); 


    roiManager("open",roi_input);
    nTotal = roiManager("Count");  
    nlabels = nTotal -nR;
    print(nlabels);
//waitForUser
    j=1; //count results
    run("Set Scale...", "distance=1 known=648.400 unit=nm global");
    
    for (r = 0; r < nR; r++){ //trough the atlas
     //information about the roi
    run("Select None");//erase previous selection
    roiManager("select",r);
    rName = Roi.getName(); 
    print(rName);
    
    //get area of the sector in mmXmm
    getStatistics(area);
    area_all_region = area/(1000000*1000000);
    
   
      run("Select None");//erase previous selection
	//
	arraySelection = ArrayIndexWithtSelectionIntersection(r,nR,nTotal);
	//add arraySelection isnot emptyADD 
	if(arraySelection.length > 0){
	roiManager("select",arraySelection);
	roiManager("measure");
	nlabels = nResults;
    nlabels = nResults;
	///
	//ADD ONCE FOUND INTERSECTION FOUND INTERSECTION WITH LEFT AND WITH RIGHT(OPPOSED THAN IN FRONT) FOUND COUNTINGS
    nlabelsRight = FindOnSector(arraySelection,indexRight);
    nlabelsLeft = FindOnSector(arraySelection,indexLeft);
    

    }
	else{
		nlabels = 0;
        nlabelsRight = 0;
        nlabelsLeft = 0;
	}
    
    areaRoiLeft = FindArea(r,indexLeft);
    areaRoiRight = FindArea(r,indexRight);
	//save in a table
	//--------------------Store results-----------
run("Clear Results");
if (j >1){
IJ.renameResults("AllLabels","Results");	
}
setResult("Brain slice", j-1 ,name_file);
setResult("Number of Labels", j-1 ,nlabels);
setResult("Area of all the ROI mmxmm",j-1, area_all_region);

setResult("Number of Labels Left", j-1 ,nlabelsLeft);
setResult("Area of Left ROI mmxmm",j-1, areaRoiLeft);

setResult("Number of Labels Right", j-1 ,nlabelsRight);
setResult("Area of Right ROI mmxmm",j-1, areaRoiRight);
setResult("Region considered",j-1, rName);

saveAs("Results",outputDir + name_file + "SummaryCounting.xls"); //intermediate result
IJ.renameResults("AllLabels");
run("Clear Results");

//waitForUser("stop");
j=j+1;
}
//save slide with roi
roiManager("reset");
selectWindow("Original");
roiManager("open",roi_input); //add the marked sector
roiManager("Set Line Width", 4);
roiManager("Show All");
run("Flatten");
rename("Flatten");
selectWindow("Flatten");
saveAs("Tiff", outputImages + name_file + "All.tif" );
//waitForUser("stop");
close("*");
close("AllLabels");
close("Log");
close("ROI Manager");
    """
    args = {
     'image_input': image_input,
     'roi_input': roi_input,
     'roi_atlas': roi_atlas,
     'outputDir' : outputDir,
     'outputImages' : outputImages,
     'scale' : float(scale)
    }
    result = ij.py.run_macro(macro, args)
    
    
    
def Create_folder(path):
    isExist = os.path.exists(path)
    if not isExist:
       # Create a new directory because it does not exist
       os.makedirs(path)