#Plot
# Set the CRAN mirror
repos <- "https://cloud.r-project.org"

# Install required packages
if (!requireNamespace("readxl", quietly = TRUE)) {
  install.packages("readxl", repos = repos)
}

if (!requireNamespace("ggplot2", quietly = TRUE)) {
  install.packages("ggplot2", repos = repos)
}

if (!requireNamespace("gridExtra", quietly = TRUE)) {
  install.packages("gridExtra", repos = repos)
}

if (!requireNamespace("xlsx", quietly = TRUE)) {
  install.packages("xlsx", repos = repos)
}

if (!requireNamespace("hrbrthemes", quietly = TRUE)) {
  install.packages("hrbrthemes", repos = repos)
}

library(hrbrthemes)
library(readxl)
library(ggplot2)
library(xlsx)
library("gridExtra")
source("X:/Users/LabSoftware/ScriptInR/RscriptsToPlotFromAtlasCounting/FindCommonRegions.R")
##### Auxiliary functions#########
plotBarPlots <- function(data){
 
    plt <- ggplot(data, aes(x = as.factor(region_considered),y=as.numeric(total_number_labels), fill = type_mice)) +
      geom_bar(position="dodge", stat="identity") + coord_flip()
   
   plt <- plt +xlab("brain region") + ylab("counts") 
    
    
 
    plt <- plt + theme(text = element_text(size=6),
                       plot.title = element_text(size=10),plot.subtitle = element_text(size=2),
                       panel.grid.major =  element_line(color = "black", size = 0.5), panel.grid.minor = element_blank(),
                       panel.background = element_blank(), axis.line = element_line(colour = "black"),
                       axis.title.x = element_text(size = 10), axis.title.y = element_text(size = 10),
                       legend.key.size = unit(1, "cm"),legend.text = element_text(size = 10) ,
                      
                       axis.text.x = element_text(size = 10),  # Adjust the size as needed
                       axis.text.y = element_text(size = 10))


    windows()
    grid.arrange(plt,nrow=1,ncol=1)
 
  return(plt)
}
####################################heat map plots
HeatMapPlots <- function(data){
  plt <- ggplot(data, aes(x = as.factor(region_considered),y=as.factor(type_mice), fill = as.numeric(total_number_labels))) +
    geom_tile() + coord_flip()+  scale_fill_gradient(low="white", high="blue",trans = "sqrt") 
   
  
   
  
  plt <- plt +xlab("brain region") + ylab("counts") 
  
  
  
  plt <- plt + theme(text = element_text(size=6),
                     plot.title = element_text(size=10),plot.subtitle = element_text(size=2),
                     panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
                     panel.background = element_blank(), axis.line = element_line(colour = "black"),
                     axis.title.x = element_text(size = 5), axis.title.y = element_text(size = 5),
                     legend.key.size = unit(1, "cm"),legend.text = element_text(size = 5) ,
                     legend.position = "right",
                     legend.direction = "vertical",
                     legend.box = "vertical",legend.title = element_blank(),
                     axis.text.x = element_text(size = 5),  # Adjust the size as needed
                     axis.text.y = element_text(size = 5))
  
  
  windows()
  grid.arrange(plt,nrow=1,ncol=1)
  
  return(plt)
}

########################## ####################
#Select file to plot

 GetExcelBarPlots<- function(selected_files){
#selected_file<-choose.files("", "Select xlsx File with counting of each ROI")

# Print the selected file path
cat("Selected file:",selected_files, "\n")
output_excel <- paste(dirname(selected_files[1]),"/","InformationForBarPlots.xlsx",sep="")
output <- paste(dirname(selected_files[1]),"/","plotsBarPlotsSeveral.pdf",sep="")

#number of sheets in the given file
sheet_names <- list()

for(indexs in c(1:length(selected_files))){
sheet_names[[indexs]]<- excel_sheets(selected_files[indexs])
}

# Call the function with your data frame
common_sheets <- find_common_values(sheet_names)


# Sort the sheet names only common sheets are considered.

sorted_sheet_names <- sort(common_sheets)
plt <- list()
index = 1
count = 1

for(s in sorted_sheet_names){
  print(s)
  #create list of data for each file
  for(indexss in c(1:length(selected_files))){
  data <- read_excel(selected_files[indexss], sheet = s)
  aux <- strsplit(selected_files[indexss],"_")
  l=aux[[1]]
  l1<-strsplit(l[length(l)],".xlsx")
  data$group <- l1
  #sum number of labels
  total_number_labels <- sum(data$`Number of Labels`)
  region_considered <- data[1,]$`Region considered`
 
  type_mice <- data[1,]$group
  resume <- data.frame(region_considered, type_mice, total_number_labels)
  colnames(resume)[2]<-"type_mice"
  
  if(count ==1){
    total <- resume
  } else{
  total <- rbind(total,resume)}
  count = count + 1
  }
 # plt[[index]] <- plotCounts(total,index)
  #index = index + 1
  
  print(s)
 }
#save in an excel file
# if(file.exists(output_excel)== 0){
# write.xlsx(total, output_excel, sheetName = "data", 
#            col.names = TRUE, row.names = TRUE, append = FALSE)}


  write.xlsx(total, output_excel, sheetName = "data", 
             col.names = TRUE, row.names = TRUE, append = FALSE)
 }

plotBars<- function(BarFile){
output <- paste(dirname(BarFile),"/","plotsBarPlotsSeveral.pdf",sep="") 
total <- read_excel(BarFile, sheet = "data")
  
#plot and same barplots
plt <- plotBarPlots(total)


windows()
ncol = 1
nrow = 1

#pdf(paste(outputdir,filePdf), width=4,height=6,paper = "a4")
pdf(output, width=20,height=100)
par(mar=c(4,0.5,0.5,0.5))
grid.arrange(plt,ncol=1,nrow=1)
#do.call("grid.arrange", c(plt, nrow = nrow,ncol=ncol))

#save(pltRel,file = outputfileRel)
dev.off()
}

###########################
##########Heat maps
HeatMap<- function(selected_file){
  output <- paste(dirname(selected_file),"/","HeatMapsPlotsSeveralvs1.pdf",sep="") 
  total <- read_excel(selected_file, sheet = "data")
  
  #plot and same barplots
  plt <- HeatMapPlots(total)
  
  
  windows()
  ncol = 1
  nrow = 1
  
  
  pdf(output, width=4,height=40)
  par(mar=c(4,0.5,0.5,0.5))
  grid.arrange(plt,ncol=1,nrow=1)

  dev.off()
  
}