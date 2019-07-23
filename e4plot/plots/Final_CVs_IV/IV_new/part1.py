import matplotlib.pyplot as plt
import math
import copy
import numpy as np 
import statistics
class get_data_values:
    """This class organises the data from a list (list is from 'part3')."""
    time = []
    number = []
    U = []
    I = []
 
    def __init__(self):
        self.time = []
        self.number = []
        self.U = []
        self.I = []
   
        self.sublist = []
        self.biglist = []
        self.av_U = []
        self.av_I = []
        self.av_U_list = []
        self.av_I_list = []
        self.av_I_err_list = []

    def update_values(self, data):
        #txt file orginally a long list of values (not columns) therefore must be separated. Text at start must be deleted.#
        
        for j in range(0,int((len(data)+1)/4)):
            #4 lists (columns)
            self.time.append(data[j*4])
            self.number.append(data[1 + j*4])
            self.U.append(data[2 + j*4])
            self.I.append(data[3 + j*4])

####################################################################################################################################
#BELOW CALCS THE AVERAGE VOLTS AND CURRENT FOR REPEATS. A MIN ERROR IS SET BELOW IF THERE IS NO REPEATS (CURRENT GOT TOO
# HIGH, PREVENTING FURTHER MEASUREMENTS) AND IS ALSO SET IF THE ERROR IS TOO SMALL. ERRORS= STANDARD DEVIATION/SQRT(NO. OF POINTS)#
        for l in range(0,int(max(self.number)+1)):
            for k in range(0, len(self.number)):
                if self.number[k] == l:
                    self.sublist.append(k)             
            self.biglist.append(self.sublist)
            self.sublist = []
        for p in self.biglist:
            for i in p:
                self.av_U_list.append(self.U[i])
                self.av_I_list.append(self.I[i])      
       
            if len(self.av_I_list) >1:    
                #THIS SETS ERROR for points but it is changed to be 0.01uA IF ERROR<0.01uA#
                if statistics.stdev(self.av_I_list)<0.01:
                    self.av_U.append(sum(self.av_U_list)/(len(self.av_U_list)))
                    self.av_I.append(sum(self.av_I_list)/(len(self.av_I_list)))
                    self.av_I_err_list.append(0.01)
                else:
                    self.av_U.append(sum(self.av_U_list)/(len(self.av_U_list)))
                    self.av_I.append(sum(self.av_I_list)/(len(self.av_I_list)))
                    self.av_I_err_list.append(float(statistics.stdev(self.av_I_list)/(len(self.av_I_list))**0.5))
            if len(self.av_I_list) == 1:   
                #THIS SETS ERROR OF 0.01uA AS STANDARD DEVIATION CANNOT BE CALC FOR LIST CONTAINING 1 VALUE#   
                self.av_U.append(self.av_U_list[0])
                self.av_I.append(self.av_I_list[0])
                self.av_I_err_list.append(0.01)

            self.av_U_list = []
            self.av_I_list = []
            

    def print_voltage(self):
        return self.av_U
    def print_time(self):
        return self.time
    def print_number(self):
        return self.number
    def print_current(self):
        return self.av_I
    def print_current_stand_dev(self):
        return self.av_I_err_list