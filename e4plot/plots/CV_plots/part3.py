import matplotlib.pyplot as plt
import math
import copy
import numpy as np 
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
        #File must not have text- must delete the headers manually.
        #Files don't have columns- just a list of values.
        self.list_of_files = os.listdir(folder_path)
        for file_a in self.list_of_files:        
            #DEPENDS ON HOW FILES ARE LABELLED#
            if "CV" and ".txt" and name_a in file_a:
                self.file_path = folder_path +"\\"+ file_a  
                self.file_paths.append(self.file_path)
        for x in self.file_paths:
            with open (x, "r") as file1:
                self.values1= []
                for line in file1:
                    for value_a in line.split():
                        self.values1.append(float(value_a))   
            return self.values1
                    