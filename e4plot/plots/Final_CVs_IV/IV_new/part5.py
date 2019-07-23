import matplotlib.pyplot as plt
import math
import copy
import numpy as np 
from part1 import get_data_values
from part3 import get_file
class get_I_and_V:
    """This class uses 'part1' and 'part3' to merge the two classes so that a list of I and V
    values are created using the folder_path and file_number. The errors used are standard deviation"""
    def __init__(self):
        self.I_values = []
        self.V_values = []
        self.cur_err = []


    def get_I(self, folder_path, file_number):
        #Gets I from the list produced in part1.
        w = get_file()
        x= w.get_file_data(folder_path, file_number)
        y= get_data_values()
        y.update_values(x)
        y.print_current()
        for a in y.print_current():
            self.I_values.append(a)
        return self.I_values
        

    def get_I_stand_dev(self, folder_path, file_number):
        #Calcs the Standard deviation/(no. of points av across) of I from the list from part1 as the error.
        w = get_file()
        x= w.get_file_data(folder_path, file_number)
        y= get_data_values()
        y.update_values(x)
        y.print_current_stand_dev()
        for a in y.print_current_stand_dev() :
            self.cur_err.append(a)
        return self.cur_err

#################################################################################

    def get_V(self, folder_path, file_number):
        #Gets V from list produced in part1.
        w = get_file()
        x= w.get_file_data(folder_path, file_number)
        y= get_data_values()
        y.update_values(x)
        y.print_voltage()
        for a in y.print_voltage():
            self.V_values.append(a)
        return self.V_values

#################################################################################