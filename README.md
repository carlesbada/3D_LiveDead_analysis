# 3D_LiveDead_analysis

This is the tutorial for installation and use of the developed 3D live-dead plugin produced under FIJI environment. This plugin has been developed to make the automatic analysis of 3D z-stacked images made from 3D cell culture live-dead analysis. Using this plugin, the defined batch of images will be automatically analysed. At the end of the process, for each given image, a new folder containing the generated data in a csv file for each image channel, a histogram with the number of counts in function of image slice, and a reconstructed z-stack image with enhanced quality for 3D visualization. 

The same process that will be described in this document can be also found in this [YouTube video](https://youtu.be/2kHNdHqRlOM). The 

### Installation
To install this plugin in FIJI, the first step that must be done is to make the actualization of FIJI. To make it, it is necessary to go to the “Help” window and run the “Update…” function. To install this plugin in FIJI, the first step that must be done is to make the actualization of FIJI. To make it, it is necessary to go to the “Help” window and run the “Update…” function. In the FIJI updater press the “Manage Update Sites” button and a new window will be opened. Press the button “Add update site” and in the new row generated at the last part of the list, add the following:

- Name: 3D LiveDead Analysis
- URL: https://sites.imagej.net/CBada/

Then press the “Close button” and the “Apply changes” on the ImageJ Updater window. At the end of the update process, restart FIJI. 


Once opened this file, save it as the recommendation made by FIJI. When the process is over, restart FIJI again and the plugin will be installed. 

### How it is used
The first thing that must be done, is to place all the images that are needed to analyse in a folder. Make sure that there are only images in this folder. Once this is done, go to the “Plugins” window, and in the last part of the list you will find “3D_LiveDead_Analysis”, click it and wait to plugin initialization. 

The first think that will be asked is to select the directory containing the images to analyse. Once this selection done, a new window will appear asking for the type of analysis (live and dead, or only live cells), and if the bio-formats plugin has been configurated. If the answer is no, a new tutorial will be launched to do this configuration. 

Then the process will start, the program will analyse each image in the given directory. The process will not be finished until a new window announcing that the process has ended appears. To check the given results, go to the folder containing the images and a new folder will has been created to each image. Inside each folder, there will be the histogram of the distribution of live and dead cells of the image in function of the slice, a new z-stack image to make a better 3D viewing, and csv files containing the data derived from the analysis for further statistical tests. 
