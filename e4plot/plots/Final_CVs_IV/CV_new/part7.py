import matplotlib.pyplot as plt
import math
import copy
import os
import numpy as np 
from part5 import get_C_and_V
import itertools
marker = itertools.cycle(( '+', '.'))
class plot_all_Cs_and_V:
    """This class plots the data from a given folder path when the file_numbers are specified. 
    batch is the sample batch. This class uses 'part5' which uses 'part1' and 'part3'."""

    def __init__(self):
        self.no_a = ''
        self.numbers = []

    def plot_all_C_V(self, folder_path, file_numbers, batch):
        #Gets C and V from a file and plots it with errors.
        #for self.no_a in file_numbers.split():
         #       self.numbers.append((self.no_a))
        for self.no_a in file_numbers:
                self.numbers.append((self.no_a))
        axis = plt.subplot()

        for number2 in self.numbers:
            # b depends on how files are labelled.
            b = batch + str(number2)
            a = get_C_and_V()
            y = a.get_C(folder_path, b)
            x = a.get_V(folder_path, b)  
            z = a.get_C_stand_dev(folder_path, b)
            
            #axis.scatter(x, y, marker = next(marker), color=np.random.rand(3,),  label= b)
            axis.errorbar(x,y,yerr=z, capsize = 5, fmt = next(marker), color =np.random.rand(3,),  label= b )

        axis.set_xlabel('Voltage (V)', fontsize=14)
        axis.set_ylabel('Capacitance $(pF)$', fontsize=14)
        axis.legend(bbox_to_anchor=(1, 0.5))
        plt.suptitle(batch)
        #plt.savefig(folder_path+'\\'+'CV'+ '_'+ batch + '_'+ file_numbers , bbox_inches ='tight', dpi=1200)
        plt.savefig(folder_path+'\\'+'CV'+ '_'+ batch + ''.join("_" + str(e) for e in file_numbers) , bbox_inches ='tight', dpi=1200)
        plt.show()
        

    def plot_all_C_squared_V(self, folder_path, file_numbers, batch):
        #Gets C and V from a file and calcs 1/C2 and plots it with errors.
        for self.no_a in file_numbers:
                self.numbers.append((self.no_a))
        axis = plt.subplot()

        for number_c in self.numbers:
            b = batch + str(number_c)
            a = get_C_and_V()
            y = a.get_C_squared(folder_path, b)
            x = a.get_V(folder_path, b)     
            z = a.get_C_squared_stand_dev(folder_path, b)
            #axis.scatter(x, y,  marker = next(marker), color=np.random.rand(3,),  label= b)
            axis.errorbar(x,y,yerr=z, capsize = 5, fmt = next(marker), color =np.random.rand(3,),  label= b )
        axis.set_xlabel('Voltage (V)', fontsize=14)
        axis.set_ylabel('$1/C^2$ $({pF})^{-2}$', fontsize=14)
        axis.legend(bbox_to_anchor=(1, 0.5))
        plt.suptitle(batch)
        plt.savefig(folder_path + '\\' + '1fracCsqrV'+ '_' + batch + ''.join("_" + str(e) for e in file_numbers) , bbox_inches='tight',dpi=1200)
        plt.show()        
        