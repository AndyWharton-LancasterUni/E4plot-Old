import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os


class Data:

    # create a data object with empty values
    def __init__(self):
        self.filled = False
        self.repeats = None
        self.n = []
        self.type = ''
        self.name = ''
        self.time = []
        self.v_mean = []
        self.i_mean = []
        self.i_error = []
        self.c_mean = []
        self.c_error = []
        self.inverse_c_squared = []
        self.inverse_c_squared_error = []
        self.temperature = []
        self.humidity = []

    # read a file and fill data
    def extract_data(self, filename):
        self.filled = True
        self.name, ext = os.path.splitext(filename)
        self.find_type()

        if self.type == 'iv':

            self.n = np.genfromtxt(fname=filename, dtype=float, usecols=1, skip_header=1).tolist()
            T = np.genfromtxt(fname=filename, dtype=float, usecols=0, skip_header=1).tolist()
            v = np.genfromtxt(fname=filename, dtype=float, usecols=2, skip_header=1).tolist()
            i = np.genfromtxt(fname=filename, dtype=float, usecols=3, skip_header=1).tolist()
            t = np.genfromtxt(fname=filename, dtype=float, usecols=4, skip_header=1).tolist()
            h = np.genfromtxt(fname=filename, dtype=float, usecols=5, skip_header=1).tolist()

            self.find_repeats()

            time_convert = []
            for x in range(0, len(T)):
                time_convert.append(T[x]-T[0])
            for x in range(0, len(time_convert), self.repeats):
                self.time.append((sum(time_convert[x:x + self.repeats]) / self.repeats))
            for x in range(0, len(v), self.repeats):
                self.v_mean.append((sum(v[x:x + self.repeats]) / self.repeats))
            for x in range(0, len(i), self.repeats):
                self.i_mean.append((sum(i[x:x + self.repeats]) / self.repeats))
            for x in range(0, len(i), self.repeats):
                self.i_error.append(stats.sem(i[x:x + self.repeats]))
            for x in range(0, len(t), self.repeats):
                self.temperature.append((sum(t[x:x + self.repeats]) / self.repeats))
            for x in range(0, len(h), self.repeats):
                self.humidity.append((sum(h[x:x + self.repeats]) / self.repeats))

        elif self.type == 'cv':

            self.n = np.genfromtxt(fname=filename, dtype=float, usecols=1, skip_header=2).tolist()
            T = np.genfromtxt(fname=filename, dtype=float, usecols='0', skip_header=1).tolist()
            v = np.genfromtxt(fname=filename, dtype=float, usecols='2', skip_header=2).tolist()
            c = np.genfromtxt(fname=filename, dtype=float, usecols='4', skip_header=2).tolist()
            t = np.genfromtxt(fname=filename, dtype=float, usecols='6', skip_header=2).tolist()
            h = np.genfromtxt(fname=filename, dtype=float, usecols='7', skip_header=2).tolist()

            self.find_repeats()

            time_convert = []
            for x in range(0, len(T)):
                time_convert.append(T[x] - T[0])
            for x in range(0, len(time_convert), self.repeats):
                self.time.append((sum(time_convert[x:x + self.repeats]) / self.repeats))
            for x in range(0, len(v), self.repeats):
                self.v_mean.append((sum(v[x:x + self.repeats]) / self.repeats))
            for x in range(0, len(c), self.repeats):
                c_repeats = c[x:x + self.repeats]
                c_final = []
                for y in range(0, len(c_repeats)):
                    if c_repeats[y] < 1e10:
                        c_final.append(c_repeats[y])
                self.c_mean.append((sum(c_final) / len(c_final)))
                self.c_error.append(stats.sem(c_final))
            for x in range(0, len(self.v_mean)):
                self.inverse_c_squared.append(1 / self.c_mean[x] ** 2)
            for x in range(0, len(self.inverse_c_squared)):
                self.inverse_c_squared_error.append((self.inverse_c_squared[x] * 2 * (self.c_error[x] / self.c_mean[x])))
            for x in range(0, len(t), self.repeats):
                self.temperature.append((sum(t[x:x + self.repeats]) / self.repeats))
            for x in range(0, len(h), self.repeats):
                self.humidity.append((sum(h[x:x + self.repeats]) / self.repeats))

        elif self.type == 'it':

            self.n = np.genfromtxt(fname=filename, dtype=float, usecols=1, skip_header=1).tolist()
            T = np.genfromtxt(fname=filename, dtype=float, usecols=0, skip_header=1).tolist()
            v = np.genfromtxt(fname=filename, dtype=float, usecols=2, skip_header=1).tolist()
            i = np.genfromtxt(fname=filename, dtype=float, usecols=3, skip_header=1).tolist()
            t = np.genfromtxt(fname=filename, dtype=float, usecols=4, skip_header=1).tolist()
            h = np.genfromtxt(fname=filename, dtype=float, usecols=5, skip_header=1).tolist()

            self.find_repeats()

            time_convert = []
            for x in range(0, len(T)):
                time_convert.append(T[x] - T[0])
            for x in range(0, len(time_convert), self.repeats):
                self.time.append((sum(time_convert[x:x + self.repeats]) / self.repeats))
            for x in range(0, len(v), self.repeats):
                self.v_mean.append((sum(v[x:x + self.repeats]) / self.repeats))
            for x in range(0, len(i), self.repeats):
                self.i_mean.append((sum(i[x:x + self.repeats]) / self.repeats)*1000000)
            for x in range(0, len(i), self.repeats):
                self.i_error.append(stats.sem(i[x:x + self.repeats])*1000000)
            for x in range(0, len(t), self.repeats):
                self.temperature.append((sum(t[x:x + self.repeats]) / self.repeats))
            for x in range(0, len(h), self.repeats):
                self.humidity.append((sum(h[x:x + self.repeats]) / self.repeats))

        else:
            print('Error')

    # Decide if file is cv, iv or it
    def find_type(self):
        if 'iv' in self.name.lower():
            self.type = 'iv'
        elif 'cv' in self.name.lower():
            self.type = 'cv'
        elif 'it' in self.name.lower():
            self.type = 'it'
            #and not ('cv' or 'iv' or 'vi' or 'vc')

    # find how many repeat measurements were done
    def find_repeats(self):
        x = 0
        measurements = 0
        for i in range(len(self.n)):
            if x == self.n[i]:
                measurements += 1
            else:
                break
        self.repeats = measurements

    # find average temperature
    def average_temp(self):
        average_temperature = sum(self.temperature) / len(self.temperature)
        temperature_error = stats.sem(self.temperature)
        return average_temperature, temperature_error

    # find average humidity
    def average_hum(self):
        average_humidity = sum(self.humidity) / len(self.humidity)
        humidity_error = stats.sem(self.humidity)
        return average_humidity, humidity_error

    # find breakdown voltage
    def breakdown_voltage(self):
        for x in range(1, len(self.i_mean) - 1):
            if abs(self.i_mean[x + 1]) >= abs(self.i_mean[x] * 1.2):
                bd_voltage = self.v_mean[x]
                return bd_voltage
                break
            else:
                continue
        else:
            return 'Breakdown not reached'

    # convert time
    def time_to_minutes(self):
        for x in range(0, len(self.time)):
            self.time[x] = self.time[x]/60

    def time_to_hours(self):
        for x in range(0, len(self.time)):
            self.time[x] = self.time[x]/3600

    def time_to_days(self):
        for x in range(0, len(self.time)):
            self.time[x] = self.time[x]/(24*3600)

    # return properties
    def get_name(self):
        return self.name

    def get_time(self, type='hours'):
        if type == 'hours':
            self.time_to_hours()
            return self.time
        elif type == 'minutes':
            self.time_to_minutes()
            return self.time
        elif type == 'days':
            self.time_to_days()
            return self.time
        else:
            return self.time

    def get_voltage(self):
        return self.v_mean

    def get_current(self):
        return self.i_mean

    def get_current_error(self):
        return self.i_error

    def get_inverse_capacitance(self):
        return self.inverse_c_squared

    def get_inverse_capacitance_error(self):
        return self.inverse_c_squared_error

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity

    # print properties
    def print_voltage(self):
        print(self.v_mean)

    def print_current(self):
        print(self.i_mean)

    def print_current_error(self):
        print(self.i_error)

    def print_temperature(self):
        print(self.temperature)

    def print_humidity(self):
        print(self.humidity)

    def print_average_temperature(self):
        print(self.average_temp())

    def print_average_humidity(self):
        print(self.average_hum())

    def print_name(self):
        print(self.name)
