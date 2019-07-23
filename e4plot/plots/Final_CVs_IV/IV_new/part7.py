import matplotlib.pyplot as plt
import math
import copy
import os
import numpy as np 
from part5 import get_I_and_V
import itertools
marker = itertools.cycle(( '+', '.'))
class plot_all_I_and_V:
    """This class plots the data from a given folder path when the file_numbers are specified. 
    batch is the sample batch. This class uses 'part5' which uses 'part1' and 'part3'."""

    def __init__(self):
        self.no_a = ''
        self.numbers = []

    def plot_all_I_V(self, folder_path, file_numbers, batch):
        #Gets I and V from a file and plots it with errors.
        for self.no_a in file_numbers:
                self.numbers.append((self.no_a))
        axis = plt.subplot()

        for number2 in self.numbers:
            # b depends on how files are labelled.
            b = batch + str(number2)
            a = get_I_and_V()
            y = a.get_I(folder_path, b)
            x = a.get_V(folder_path, b)  
            z = a.get_I_stand_dev(folder_path, b)
            axis.errorbar(x, y, yerr=z, capsize = 5, fmt = next(marker), color =np.random.rand(3,), label= b)

        axis.set_xlabel('Voltage (V)', fontsize=14)
        axis.set_ylabel('Current $(uA)$', fontsize=14)
        axis.legend(bbox_to_anchor=(1, 0.5))
        plt.suptitle(batch)
        plt.savefig(folder_path +'\\'+'IV'+ '_'+ batch + ''.join("_" + str(e) for e in file_numbers) , bbox_inches='tight', dpi=1200)
        plt.show()
        


        