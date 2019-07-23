'part9': Uses argparse to plot CV and 1/CsquaredV from CMD line. 
	 Requires 3 arguments: folder path, sample, file no..
'final': Uses all the other classes. It requires 3 arguments: folder path, file no., sample.
'part7': Plots a graph when called in final.
'part5': Uses 'part1' and 'part3' classes to produce lists of voltages and capacitances and 
	 errors for a given file.
'part1': Class reads one long list returns organised lists (voltages, capactiances...).
'part3': It opens a file and creates a list of floats that is combined with 'part1' in 'part5'.

##################################################################################################

In CMD:
Type first:
cd C:\Users\nikit\Documents\GaAs\CV_plots\CV_new
Then:
python part9.py C:\\Users\\nikit\\Documents\\GaAs\\share\\V1\\scratch\\2 B9Ba 1 11 2 12 

#This will plot the contacts 1,11,2,12 from sample B9Ba on the same plot and save the CV and 
1/CsquaredV graphs in the folder path used to get the data.

##################################################################################################

#IMPROVEMENTS: Part1 and Part3 could be merged? In Part1, genfromtxt columns are put into 1 long
	       list that is then passed to Part3 to create separate lists representing columns. 		

	       Possibly merge IV and CVs into one program?

	       IV has the same structure.