import matplotlib.pyplot as plt
import math
import copy
import numpy as np 
from part1 import get_data_values
from part3 import get_file
class get_C_and_V:
    """This class uses 'part1' and 'part3' to merge the two classes so that a list of C, V and 1/C2 
    values are created using the folder_path and file_number. The errors used are standard deviation"""
    def __init__(self):
        self.C_values = []
        self.V_values = []
        self.C_squared_values = []
        self.n_values = []
        self.cap_err = []
        self.cap_sq_err = []

    def get_C(self, folder_path, file_number):
        #Gets C from the list produced in part1.
        w = get_file()
        x= w.get_file_data(folder_path, file_number)
        y= get_data_values()
        y.update_values(x)
        capacitance = y.print_capacitance()
        for a in capacitance:
            cap = a
            self.C_values.append(cap)
        return(self.C_values)

    def get_C_stand_dev(self, folder_path, file_number):
        #Calcs the Standard deviation of C from the list from part1.
        w = get_file()
        x= w.get_file_data(folder_path, file_number)
        y= get_data_values()
        y.update_values(x)
        capacitance_err = y.print_capacitance_stand_dev()
        for a in capacitance_err:
            cap_err = a
            self.cap_err.append(cap_err)
        return(self.cap_err)
#################################################################################

    def get_V(self, folder_path, file_number):
        #Gets V from list produced in part1.
        w = get_file()
        x= w.get_file_data(folder_path, file_number)
        y= get_data_values()
        y.update_values(x)
        voltage = y.print_voltage()
        for a in voltage:
            volt = a
            self.V_values.append(volt)
        return(self.V_values)
#################################################################################
    #For file to open:Filename= CV with Batch+file_number 
    def get_C_squared(self, folder_path, file_number):
        #Gets C from list from part1, squares each value and adds to a new list to be plotted.
        w = get_file()
        x= w.get_file_data(folder_path, file_number)
        y= get_data_values()
        y.update_values(x)
        capacitance = y.print_capacitance()
        for a in capacitance:
            capacitance_squared = 1/(a*a)
            self.C_squared_values.append(capacitance_squared)
        return(self.C_squared_values)

    def get_C_squared_stand_dev(self, folder_path, file_number):
        #Calcs 1/C2 error
        w = get_file()
        x= w.get_file_data(folder_path, file_number)
        y= get_data_values()
        y.update_values(x)
        capacitance_err = y.print_capacitance_stand_dev()
        capacitance = y.print_capacitance()
        for i in range(0, len(capacitance_err)):
            cap_sq_err1 = 2*(capacitance_err[i]*capacitance[i])
            self.cap_sq_err.append(cap_sq_err1)
        return(self.cap_sq_err)