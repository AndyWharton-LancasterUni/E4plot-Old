import matplotlib.pyplot as plt
import math
import copy
import os
import numpy as np 
from part7 import plot_all_Cs_and_V

#This uses 4 classes to produce the CV graphs. FILE FROM FOLDER MUST CONTAIN 'CV','.txt', AND 'batch + number'.
#FILE.txt MUST HAVE NO TEXT. Aruments:(folder path, contact numbers, batch). Can be changed in 'part3'.
######################################################################################################################################

#The two lines below plot graphs

#plot_all_Cs_and_V().plot_all_C_V('C:\\Users\\nikit\\Documents\\GaAs\\share\\V1\\scratch\\2', '1 11 2 12', 'B9Ba')    
#plot_all_Cs_and_V().plot_all_C_squared_V('C:\\Users\\nikit\\Documents\\GaAs\\share\\V1\\scratch\\2', '1 2 3 5 7 8 9 10 11 12 13 14 17', 'B9Ba')

class final:
    """This class uses all of the other classes to plot CV and C_squaredV graphs for multiple contacts in the same sample."""
    def final1(self,folderpath, files, sample):
        plot_all_Cs_and_V().plot_all_C_V(folderpath, files, sample)
    def final2(self,folderpath, files, sample):
        plot_all_Cs_and_V().plot_all_C_squared_V(folderpath, files, sample)