import matplotlib.pyplot as plt
import math
import copy
import numpy as np 
import os
import glob2
class get_file:
    """This class creates one list containing all of the data using a folder_path and the file number"""
    def __init__(self):
        self.list_of_files = []
        self.values1 = []
        self.file_path = ''
        self.file_paths = []
        
    """def get_file_data(self, folder_path, name_a):
        #Opens a txt file if contains IV and number (name_a) and creates 1 long list of values.
        #File must not have text- must delete the headers manually.
        #Files don't have columns- just a list of values.
        self.list_of_files = os.listdir(folder_path)
        for file_a in self.list_of_files:        
            #DEPENDS ON HOW FILES ARE LABELLED#
            if "IV" and ".txt" and name_a in file_a:
                self.file_path = folder_path +"\\"+ file_a  
                self.file_paths.append(self.file_path)
        for x in self.file_paths:
            with open (x, "r") as file1:
                self.values1= []
                for line in file1:
                    for value_a in line.split():
                        self.values1.append(float(value_a))   
            return self.values1"""
            
    def get_file_data(self, folder_path, name_a):
        mydir = folder_path
        file_list = glob2.glob(mydir + "/*.txt") 
        y = file_list
        file_listIV =[]
        for x in y:
            if "IV" and ".txt" and name_a in x and "_short" not in x:
                file_listIV.append(x[(len(mydir)+3):-4])
                self.values1 = []
                a= np.genfromtxt(fname=x, dtype= float, usecols=0, skip_header=1)
                b= np.genfromtxt(fname=x, dtype= float, usecols=1, skip_header=1)
                c= np.genfromtxt(fname=x, dtype= float, usecols=2, skip_header=1)
                d= np.genfromtxt(fname=x, dtype= float, usecols=3, skip_header=1)
                for x in range(0,len(a)):
                    self.values1.append(a[x])  
                    self.values1.append(b[x])  
                    self.values1.append(c[x])  
                    self.values1.append(d[x])  
                return(self.values1)
        #print(file_listIV)
