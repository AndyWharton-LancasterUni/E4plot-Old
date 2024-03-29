# Graph_Plotting

Graph plotting is a software that allows the user to plot data produced by e4Control.

## Usage

There are two executable files in Graph_Plotting. 
These are Plot_Multiple.py and Plot_Single.py

Both of these allow the user to plot current against voltage (IV), inverse capacitance squared against voltage (CV) and current against time (It) graphs. All the graphs can be plotted with or without temperature and humidity data. It is possible to find the breakdown voltage on the IV graphs, the full depletion voltage on the CV and the stability of the current on It graphs.

### Plot_Multiple.py

Plot_Multiple.py requires one input, the path to the directory containing the data files.

Run it in the command line:

`python Plot_Multiple.py file_directory -o output_directory -iv plot_iv -cv plot_cv -it plot_it -ivth plot_ivth -cvth plot_cvth -itth plot_itth -iv_f plot_ivf -cv_f plot_cvf -it_f plot_itf -av choose_average`

* Required Inputs
    *  file_directory --> The directory containing the data to be plotted
* Optional Inputs
    *  output_directory --> The directory where you want to save the plots, default is the file directory.
    *  plot_iv --> This will controls whether IV graphs are plotted, the default is yes, to switch off enter `n`
    *  plot_cv --> This will controls whether CV graphs are plotted, the default is yes, to switch off enter `n` 
    *  plot_it --> This will controls whether It graphs are plotted, the default is yes, to switch off enter `n` 
    *  plot_ivth --> This will controls whether IV graphs are plotted with temperature and humidity, the default is yes, to switch off enter `n`
    *  plot_cvth --> This will controls whether CV graphs are plotted with temperature and humidity, the default is yes, to switch off enter `n`
    *  plot_ivth --> This will controls whether It graphs are plotted with temperature and humidity, the default is yes, to switch off enter `n`      
    *  plot_ivf --> This will controls whether IV graphs are plotted with appropriate fits, the default is yes, to switch off enter `n`
    *  plot_cvf --> This will controls whether cv graphs are plotted with appropriate fits, the default is yes, to switch off enter `n`
    *  plot_itf --> This will controls whether it graphs are plotted with appropriate fits, the default is yes, to switch off enter `n`
    *  choose_average --> This decides whether to calculate the current and/or capacitance using the mean or the median, the default is mean, to change enter `median`
    
Example: `python Plot_Multiple.py <path_to_folder_1> -o <path_to_folder_2> -it n -iv_th n -cv_f n` 
  
The above example will plot all IV and CV data in folder 1 and save the plots in separate IV and CV folders in folder 2, It data will not be plotted. The IV graphs will not have temperature and humidity lines while the CV graphs will not have fits on them.
  
**Important: In order for Plot_Multiple.py to work, all the text files need to contain one of 'iv', 'cv' or 'it' (not case sensitive) in the file name. If not use Plot_Single.py**

### Plot_Single.py 

Plot_Single.py requires one input, the path to the file you wish to plot.

Run it in the command line:

`python Plot_Single.py file_path -n name -o output_directory -t plot_type  -th plot_temp_and_hum -f plot_fits -av choose_average -r remove_anomalous`

* Required Inputs
    *  file_path --> The path to the file containing the data to be plotted (including .txt)
* Optional Inputs
   *  output_directory --> The directory where you want to save the plots, default is the file directory
   *  name -->  The name and title of the graph produced, default is the file name
   *  plot_type --> Use when the filename does not contain the data type, enter `iv`, `cv` or `it`
   *  plot_temp_and_hum --> Controls if the graph is plotted with temperature and humidity, the default is yes, to switch off enter `n`
   *  plot_fits --> Include the appropriate fit for the graph the default is yes, to switch off enter `n`
   *  choose_average --> This decides whether to calculate the current and/or capacitance using the mean or the median, the default is mean, to change enter `median`
   * remove_anomalous --> This prevents certain points being plotted, enter the index of the point(s) that should be ignored. Remember that python counts from 0.

Example: `python Plot_Single.py <path_to_folder/Sensor.txt> -n "Sensor IV Curve" -t iv -th n -r 5`

This will plot an IV curve with the breakdown voltage plotted but no temperature and humidity lines and will save it in an IV folder in the same folder as the data. The title will be Sensor IV Curve. It will not plot the 6th data point.

## Improvements

This code is not complete and still has areas which can be improved:

1. The method for dealing with booleans in the parser can be improved
2. Currently finding the depletion voltage requires points with unreasonably small or large errors to be neglected, there may be a better way to do this 
3. The method for removing data points with very small errors when doing the CV fits could probably be shortened.
4. Calculating the median is still not implemented perfectly and often crashes
5. The fits for the It curve does not currently have a way of ignoring any anomalous points  
6. Some of the values that are calculated with errors are not always rounded to the correct number of significant figures
7. Being able to plot multiple graphs on one axis may be useful however this has not been implemented
