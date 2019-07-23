import matplotlib.pyplot as plt
import math
import copy
import numpy as np 
import glob2
import os
class get_file:
    """This class creates one list containing all of the data using a folder_path and the file number"""
    def __init__(self):
        self.list_of_files = []
        self.values1 = []
        self.file_path = ''
        self.file_paths = []
        
    def get_file_data(self, folder_path, name_a):
        #Opens a txt file if contains CV and number (name_a) and creates 1 long list of values.
        mydir = folder_path
        file_list = glob2.glob(mydir + "/*.txt") 
        y = file_list
        file_listIV =[]
        for x in y:
            if "CV" and ".txt" and name_a in x and "_short" not in x:
                file_listIV.append(x[(len(mydir)+3):-4])
                self.values1 = []
                a= np.genfromtxt(fname=x, dtype= float, usecols=0, skip_header=2)
                b= np.genfromtxt(fname=x, dtype= float, usecols=1, skip_header=2)
                c= np.genfromtxt(fname=x, dtype= float, usecols=2, skip_header=2)
                d= np.genfromtxt(fname=x, dtype= float, usecols=3, skip_header=2)
                e= np.genfromtxt(fname=x, dtype= float, usecols=4, skip_header=2)
                f= np.genfromtxt(fname=x, dtype= float, usecols=5, skip_header=2)
                for x in range(0,len(a)):
                    self.values1.append(a[x])  
                    self.values1.append(b[x])  
                    self.values1.append(c[x])  
                    self.values1.append(d[x]) 
                    self.values1.append(e[x])  
                    self.values1.append(f[x])  
                return(self.values1)
                    