
# 3D_Confocal_LiveDead_analysis
# Developed by Carles Bada
# Automatic particle quantification for fluorescent images for a live/dead analysis

# The following code describes the process of making an automatic live/dead quantification
# giving as result: csv files with the volume and the position of the particles, an histogram
# of the particle distribution in z-axis for live and dead channels, and a 3D z-stack image 
# with the particle surfaces and centres of masses of both analysis.


# Imported packages and classes
from ij import IJ, WindowManager
from ij.gui import GenericDialog, Plot, NonBlockingGenericDialog
from ij.process import LUT
from ij.plugin import ZProjector, filter
from java.io import File
from ij.measure import ResultsTable
import os
from org.jfree.chart import ChartFactory, ChartPanel, plot, ChartUtils
from org.jfree.data.statistics import HistogramDataset, HistogramType  
from javax.swing import JFrame  
from java.awt import Color
import array as ar  
import time


def image_importer(): # Fucntion for imporing the directory and the list of images
	directory = IJ.getDirectory("Choose a Directory "); 
	img_list = os.listdir(directory);
	os.chdir(directory);
	return directory,img_list

def user_dialog_format(): # Basic dialog for selecting the analysis type and Bio-Formats configuration
	gui = GenericDialog("Previuos considerations"); 
	gui.addChoice("Choose analysis type", ["Normal", "Only live cells"], "Normal"); 
	gui.addChoice("Have you configured bio-formats?", ["YES", "NO"], "YES"); 
	gui.addMessage("If you are not sure, mark NO");
	gui.showDialog();
	
	if gui.wasOKed(): # if was Oked, sabe the answers
		culture_type = gui.getNextChoice(); 
		bio_formats = gui.getNextChoice(); 
		
		if bio_formats=="NO": # if Bio-Formats is not configurated, open the plugin and the tutorial
			IJ.run("Bio-Formats Plugins Configuration", "");
			tutorial = NonBlockingGenericDialog("Follow this instructions: "); 
			tutorial.addMessage("1. In the formats window find your image format in the list");
			tutorial.addMessage("2. Make sure enable and windowless is activated");
			tutorial.addMessage("3. Close the bio-formats window");
			tutorial.addMessage("4. Press OK!");
			tutorial.showDialog();
		
	return (culture_type)


def image_opener(directory,img_open): # function for opening the image 
	IJ.open(directory+img_open); 
	imp = WindowManager.getCurrentImage(); 
	dim=imp.getDimensions(); # get dimensions
	n_slices = dim[3] # get the number of slices
	if (dim[2]>1): # if the number of channels is higher than 1, split channels
		IJ.run("Split Channels"); 
	else: 
		pass
		
	img_pre_opened=WindowManager.getImageTitles(); # actual openned images
	for img in img_pre_opened:
			imp = WindowManager.getImage(img); 
			lut=imp.getLuts(); # get the LUT of the image
			for lut_item in lut:
				lut_str = str(lut_item);
				if "green" in lut_str: # if green add Live label
					IJ.selectWindow(img); 
					IJ.run ('Rename...', 'title=Live-'+img);
				if "red" in lut_str: # if red add Dead label
					IJ.selectWindow(img);
					IJ.run ('Rename...', 'title=Dead-'+img);
				else:
					continue
					
	img_opened=WindowManager.getImageTitles(); # list with opened images with actual names
	return (img_opened,n_slices)

def newFolder(directory,img_open): # creates a new folder with the name of the image
	newFolderDir = directory + "Analysis_" + img_open+'/';
	if not os.path.exists(newFolderDir):
		os.makedirs(newFolderDir); 
	os.chdir(newFolderDir);
	return newFolderDir	

def image_processing(img_opened, culture_type): # Function for the analysis of each image
	IJ.run("3D OC Options", "volume centre_of_mass dots_size=10 font_size=20 store_results_within_a_table_named_after_the_image_(macro_friendly) redirect_to=none");
	# 3D OC options configuration
	
	for img in img_opened:
			
		imp = IJ.selectWindow(img); # image filtering
		IJ.run(imp, "Minimum...", "radius=1 stack");
		IJ.run(imp, "Maximum...", "radius=1 stack");
		IJ.run(imp, "Maximum...", "radius=1 stack");
		
		# To avoid non-particles problems: make a z-project and detect if there are or not particles
		IJ.run(imp, "Z Project...", "projection=[Average Intensity]");
		img_opened=WindowManager.getImageTitles();
		for name in img_opened:
			if "AVG" in name:
				IJ.selectWindow(name);
				IJ.run(imp, "Find Maxima...", "prominence=1 output=Count"); #
				IJ.selectWindow(name); 
				IJ.run("Close"); 
				time.sleep(1.5);
				print("Detecting particles...")
				rt = ResultsTable.getResultsTable();
				count = rt.getColumn(0);
				count_l = [count[-1]];
	
		imp = IJ.selectWindow(img);
		
		min_size = "50"; # default size filter

		if culture_type == "Only live cells":
			if "Live" in img:
				min_size = "100"; # filter for live cells
				if count_l[0]>1:
					print("Analysing channel...");
					IJ.run(imp, "3D Objects Counter",
					" threshold=1" + " min.="+min_size+" max.=6638 exclude_objects_on_edges" +
		  			" surfaces centres_of_masses" +
		  			" statistics")  
				else:
					print("Analysing channel...")
					IJ.run(imp, "3D Objects Counter",
					" min.="+min_size+" max.=6638 exclude_objects_on_edges" +
		  			" surfaces centres_of_masses" +
		  			" statistics") 
				time.sleep(0.8)
		else: 
			if "Live" in img: 
				min_size = "100";
			if count_l[0]>1:
				print("Analysing channel...");
				IJ.run(imp, "3D Objects Counter",
				" threshold=1" + " min.="+min_size+" max.=6638 exclude_objects_on_edges" +
	  			" surfaces centres_of_masses" +
	  			" statistics")
			else:
				print("Analysing channel...")
				IJ.run(imp, "3D Objects Counter",
				" min.="+min_size+" max.=6638 exclude_objects_on_edges" +
	  			" surfaces centres_of_masses" +
	  			" statistics") 
			time.sleep(0.8)
		IJ.selectWindow(img); 
		IJ.run("Close"); 
		
	img_analysed=WindowManager.getImageTitles(); 
	return img_analysed

def histogramer(NewFolderDir,n_slices): # Function for saving the results and making the histogram
	non_img_list = WindowManager.getNonImageTitles(); 
	Z_M = []; # 
	for non_img in non_img_list:
		if "Statistics" in non_img:
			print("Saving data...")
			rt = WindowManager.getWindow(non_img).getTextPanel().getOrCreateResultsTable(); # save the results in a results table
			index = rt.getColumnIndex("ZM"); # 
			z_m_i = rt.getColumn(index); # get ZM column
			if "Live" in non_img or "Dead" in non_img:
				rt.saveAs(NewFolderDir+non_img+'.csv'); # save the data
				z_m_double = ar.array('d',[]);
				for value in z_m_i:
					z_m_double.append(value);	
				Z_M.append(z_m_double); 
			else:
				continue 
			
	hist = HistogramDataset(); # generate the dataset
	hist.setType(HistogramType.FREQUENCY); # select type of histogram
	channels = ["Live","Dead"]; 
	i = 0;
	for data_set in Z_M:
		hist.addSeries(channels[i], data_set, n_slices,0,n_slices); # generate each serie
		i+=1;
		
	chart = ChartFactory.createHistogram("Live-Dead along Z-axis", "Depth", "Counts", hist, plot.PlotOrientation.VERTICAL, True, True, False); # histogram configuration
	chart.getXYPlot().getRendererForDataset(hist).setSeriesPaint(1, Color.red)
	chart.getXYPlot().getRendererForDataset(hist).setSeriesPaint(0, Color.green)
	chart.plot.setForegroundAlpha(0.5);
	
	w = 640;
	h = 480;
	directory_img = File(NewFolderDir + "Histogram.png");
	print("Histogram completed");
	ChartUtils.saveChartAsPNG( directory_img , chart , w , h ); # save histogram

def reconstruction_3d(img_analysed, newFolderDir,culture_type): # function for 3D reconstruction after the analysis
	if culture_type == "Only live cells":
		for img in img_analysed:
			imp = IJ.selectWindow(img); #seleccionem la primera imatge de la llista
			IJ.run(imp, "8-bit", "");
			if "Centres of mass" in img:
				if "Live" in img:
					c7 = img;
			if "Surface map" in img:
				if "Live" in img: 
					c2 = img;
			else:
				continue
				
		IJ.run("Merge Channels...", "c2=["+c2+"] c7=["+c7+"] create ignore");

	else:
		for img in img_analysed:
			imp = IJ.selectWindow(img); #seleccionem la primera imatge de la llista
			IJ.run(imp, "8-bit", "");
			if "Centres of mass" in img:
				if "Dead" in img:
					c6 = img;
			if "Centres of mass" in img:
				if "Live" in img:
					c7 = img;
			if "Surface map" in img:
				if "Dead" in img:
					c1 = img;
			if "Surface map" in img:
				if "Live" in img: 
					c2 = img;
			else:
				continue
		IJ.run("Merge Channels...", "c1=["+c1+"] c2=["+c2+"] c6=["+c6+"] c7=["+c7+"] create ignore");

		
	IJ.saveAs("Tiff", newFolderDir+"live_dead_3d.tiff");
	print("Reconstruction complete");
	

def closer(): # Function for closing images to save memory over the process
	IJ.run("Close All", "OK");
	statistics_open = WindowManager.getNonImageTitles();
	for stat in statistics_open:
		IJ.selectWindow(stat); 
		IJ.run ('Close');

def process_completed(): # End dialog function
	gui = GenericDialog("End"); 
	gui.addMessage("Process ready!");
	gui.addMessage("Check your results in the image directory");
	gui.showDialog();
	
def main(): # function that organizes the whole plugin
	directory,img_list=image_importer(); # define directory
	culture_type=user_dialog_format(); # previous consideretions
	for img_open in img_list: # for each image in the directory...
		print("Processing image: "+img_open);
		newFolderDir=newFolder(directory,img_open); # create a new folder
		img_opened,n_slices=image_opener(directory,img_open); # open the image
		img_analysed=image_processing(img_opened,culture_type); # process and analyse it
		histogramer(newFolderDir,n_slices); # make the histogram
		reconstruction_3d(img_analysed,newFolderDir,culture_type); # make the new 3D image
		print("\\Clear");
		closer(); # close windows
	process_completed(); # end of the process
	
main()

