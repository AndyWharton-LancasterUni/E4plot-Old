import matplotlib.pyplot as plt
import math
import copy
import os
import numpy as np 
from part7 import plot_all_I_and_V

#This uses 4 classes to produce an IV graph. FILE FROM FOLDER MUST CONTAIN 'IV','.txt', AND 'batch + number'.
#Aruments:(folder path, contact numbers, batch). Can be changed in 'part3'.
######################################################################################################################################

#The two lines below plot graphs

class final:
    """This class uses all of the other classes to plot an IV graph for multiple contacts in the same sample."""
    def final1(self,folderpath, files, sample):
        plot_all_I_and_V().plot_all_I_V(folderpath, files, sample)


#final().final1("C:\\Users\\nikit\\Documents\\GaAs\\share\\V1\\scratch\\2", "1 11 2 12", "B9Ba")
