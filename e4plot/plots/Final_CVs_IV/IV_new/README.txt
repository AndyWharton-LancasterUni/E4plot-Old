'part9': Uses argparse to plot IV graph from CMD line. 3 arguments: folder path, sample, file no..
'final': Uses all the other classes. It requires 3 arguments: folder path, file no., sample.
'part7': Plots a graph using 'part5' when called in final.
'part5': Uses 'part1' and 'part3' classes to produce lists of voltages and currents and 
	errors for a given file.
'part1': Class reads one long list returns separated lists (voltages, currents...).
'part3': It opens a file and creates a list of floats that is combined with 'part1' in 'part5'.

##################################################################################################

In CMD:
First:
cd C:\Users\nikit\Documents\GaAs\CV_plots\IV_new
Then:
python part9.py C:\\Users\\nikit\\Documents\\GaAs\\share\\V1\\scratch\\2 B9Ba 1 11 2 12

This plots contacts 1,11,2,12 from sample B9Ba onto one graph that is saved in the directory given.

#################################################################################################

IMPROVEMENTS: in CV README.txt


