 
 ////////////////////////////////////////Function////////////////////


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
		roiManager("select",indexSector);
		 getStatistics(area);
         areaRoi = area/(1000000*1000000);
		}
	return areaRoi;
}

/////////////////////////////////////////////////BEGIN PROGRAM//////////////////////////////////////////////////////
//open slice
//open roi
//open roi atlas
// combine roi and save it as .roi
image_input ="X:/Users/Members/Yael_Kashash/ABBA_BMR4_full/Cfos/170_BMR4_Slide17_03.tif";
scale = 648.4;
StainCell = "Cfos";
roi_input ="X:/Users/Members/Yael_Kashash/ABBA_BMR4_full/Roi_all_image/170_BMR4_Slide17_03.zip";
roi_atlas = "X:/Users/Members/Yael_Kashash/ABBA_BMR4_full/ROI_From_Atlas/RoiSet170_BMR4_Slide17_03.zip";
outputDir ="X:/Users/Members/Yael_Kashash/ABBA_BMR4_full/"+ "/CountingResultOf" + StainCell  + "/";
outputImages ="X:/Users/Members/Yael_Kashash/ABBA_BMR4_full/"+ "/LabeledImagesOf" + StainCell  + "/";
/*inputData =  getArgument();

data =split(inputData,"%");
roi_input = data[0];
roi_atlas = data[1];
outputDir = data[2];
outputImages = data[3];
image_input = data[4];
StainCell = data[5];*/



name_file =substring(image_input, lastIndexOf(image_input, "/")+1, lastIndexOf(image_input, "."));

print("Wait  "+name_file);
setBatchMode(true);
//Open the image
open(image_input);
run("Set Scale...", "distance=1 known=648.4 unit=nm global");
rename("Original");  
//open roi atlas 
 roiManager("reset");
 roiManager("open",roi_atlas);
 nAtlas = roiManager("Count");  // number of ROI of atlas.
  //Find Left /Right of the atlas
 indexLeft = FindSector(nAtlas,"Left"); //left is actually right
 indexRight = FindSector(nAtlas,"Right"); 
 //add to roi manager rois of the images
roiManager("open",roi_input);
 nTotal = roiManager("Count");  
 nlabels = nTotal -nAtlas;
///Create empty arrays with the size of atlas roi
array_labels = newArray(nAtlas);
array_areas = newArray(nAtlas);
array_names = newArray(nAtlas);
array_areas_Left = newArray(nAtlas);
array_labels_Left = newArray(nAtlas);
array_areas_Right = newArray(nAtlas);
array_labels_Right = newArray(nAtlas);

//fill areas and names from the atlas
for (r = 0; r < nAtlas; r++){
    run("Select None");//erase previous selection
    roiManager("select",r);
    rName = Roi.getName(); 
    //print(rName);
    //get area of the sector in mmXmm
    getStatistics(area);
    area_all_region = area/(1000000*1000000);
    //save in the arrays
    array_names[r] = rName;
    array_areas[r] = area_all_region;
    array_areas_Left[r]=FindArea(r,indexLeft);
    array_areas_Right[r] =FindArea(r,indexRight);
   }
//print(nlabels);
count=0;
//Find the location of each label
// loop through label
for (vr1 = nAtlas; vr1 < (nTotal-1); vr1++){
	///check area cfos
	//roiManager("select", vr1);
	//getStatistics(area);
	//area_cfos = area;
	//roiManager("deselect");
	/////
	print("\\Clear");
	print("working "+ name_file + "  "+ vr1);
   //loop through the atlas only for big detections
  //if(area_cfos > 100){
   for (r = 0; r < nAtlas; r++){
   //all the sector
   roiManager("select",newArray(r,vr1));
   roiManager("AND"); //find joining
   if (selectionType > -1 ){// if it is overlapped
         array_labels[r] = array_labels[r] + 1;
         }
    //all left sector
    roiManager("select",newArray(r,vr1,indexLeft));
    roiManager("AND"); //find joining
    if (selectionType > -1 ){// if it is overlapped
         array_labels_Left[r] = array_labels_Left[r] + 1;
         }
    
    //all right sector
    roiManager("select",newArray(r,vr1,indexRight));
    roiManager("AND"); //find joining
    if (selectionType > -1 ){// if it is overlapped
         array_labels_Right[r] = array_labels_Right[r] + 1;
         }
   }
//}
// print(count);
 count = count + 1;

}


j=1; //save results 

for (r = 0; r < nAtlas; r++){ //trough the atlas

setResult("Brain slice", j-1 ,name_file);
setResult("Number of Labels", j-1 ,array_labels[r]);
setResult("Area of all the ROI mmxmm",j-1, array_areas[r]);


setResult("Number of Labels Left", j-1 ,array_labels_Left[r]);
setResult("Area of Left ROI mmxmm",j-1,array_areas_Left[r]);

setResult("Number of Labels Right", j-1 ,array_labels_Right[r]);
setResult("Area of Right ROI mmxmm",j-1,array_areas_Right[r]);

setResult("Region considered",j-1, array_names[r]);

//saveAs("Results",outputDir + name_file + "SummaryCounting.xls"); //intermediate result

j=j+1;

}
saveAs("Results",outputDir + name_file + "SummaryCounting.xls");
//saveAs("Results",outputDir + name_file + "SummaryCountingvs4.xls"); //intermediate result

//save slide with roi
roiManager("reset");
selectWindow("Original");
roiManager("open",roi_input); //add the marked sector
roiManager("Set Line Width", 2);
run("Flatten");
saveAs("Tiff", outputImages + name_file + "All.tif" );
close("*");
close("Results");
close("ROI Manager");
setBatchMode(false);
print("Finish  " +  name_file);
close("Log");
run("Quit");