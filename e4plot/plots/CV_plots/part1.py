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
    C = []
    Rlcr = []
    def __init__(self):
        self.time = []
        self.number = []
        self.U = []
        self.I = []
        self.C = []
        self.Rlcr = []

        self.sublist = []
        self.biglist = []
        self.av_U = []
        self.av_C = []
        self.av_U_list = []
        self.av_C_list = []
        self.av_C_err_list = []

    def update_values(self, data):
        #txt file orginally a long list of values (not columns) therefore must be separated. Text at start must be deleted.#
        
        for j in range(0,int((len(data)+1)/6)):
            #6 lists (columns)
            self.time.append(data[j*6])
            self.number.append(data[1 + j*6])
            self.U.append(data[2 + j*6])
            self.I.append(data[3 + j*6])
            self.C.append(data[4 + j*6])
            self.Rlcr.append(data[5 + j*6])
####################################################################################################################################
#BELOW CALCS THE AVERAGE VOLTS AND CAPACITANCE FOR REPEATS. A MIN ERROR IS SET BELOW IF THERE IS NO REPEATS (CURRENT GOT TOO
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
                self.av_C_list.append(self.C[i])      

            #self.av_U.append(sum(self.av_U_list)/(len(self.av_U_list)))
            #self.av_C.append(sum(self.av_C_list)/(len(self.av_C_list)))
            #self.av_C_err_list.append(statistics.stdev(self.av_C_list))

            if len(self.av_C_list) >1:    
                #THIS SETS ERROR for points but it is changed to be 5pF IF ERROR<5#
                if statistics.stdev(self.av_C_list)<5:
                    self.av_U.append(sum(self.av_U_list)/(len(self.av_U_list)))
                    self.av_C.append(sum(self.av_C_list)/(len(self.av_C_list)))
                    self.av_C_err_list.append(5)
                else:
                    self.av_U.append(sum(self.av_U_list)/(len(self.av_U_list)))
                    self.av_C.append(sum(self.av_C_list)/(len(self.av_C_list)))
                    self.av_C_err_list.append(statistics.stdev(self.av_C_list)/(len(self.av_C_list))**0.5)
            if len(self.av_C_list) == 1:   
                #THIS SETS ERROR OR 5pF AS STANDARD DEVIATION CANNOT BE CALC FOR LIST CONTAINING 1 VALUE#   
                self.av_U.append(self.av_U_list[0])
                self.av_C.append(self.av_C_list[0])
                self.av_C_err_list.append(5)

            self.av_U_list = []
            self.av_C_list = []


    def print_voltage(self):
        return self.av_U
    def print_time(self):
        return self.time
    def print_number(self):
        return self.number
    def print_current(self):
        return self.I
    def print_capacitance(self):
        return self.av_C
    def print_rlcr(self):
        return self.Rlcr
    def print_capacitance_stand_dev(self):
        return self.av_C_err_list