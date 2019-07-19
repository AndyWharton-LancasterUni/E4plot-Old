import matplotlib.pyplot as plt
from Get_Data import Data
import Fitting
import os


class Plot:

    def __init__(self):
        self.fig = plt.figure()

    def plot_graph(self, output_folder, th, fits, data=Data()):
        self.add_axes(th=th)
        if data.type == 'it':
            self.plot_it(th, fits, data)
        elif data.type == 'cv':
            self.plot_cv(th, fits, data)
        elif data.type == 'iv':
            self.plot_iv(th, fits, data)
        self.save_graph(output_folder, data)

    def make_patch_spines_invisible(ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)

    def add_axes(self, th=False):
        if th:
            self.fig.host = self.fig.add_subplot()
            self.fig.subplots_adjust(right=0.75)

            self.fig.temp = self.fig.host.twinx()
            self.fig.hum = self.fig.host.twinx()

            self.fig.hum.spines["right"].set_position(("axes", 1.2))
            Plot.make_patch_spines_invisible(self.fig.hum)
            self.fig.hum.spines["right"].set_visible(True)
        else:
            self.fig.host = self.fig.add_subplot()

    def plot_it(self, th, fits, it=Data()):
        it.time_to_hours()

        current_line = self.fig.host.errorbar(x=it.time, y=it.i_mean, yerr=it.i_error, fmt='r.', label='Current')
        self.fig.host.set_ylim([min(it.i_mean) * 1.1, 0])
        self.fig.host.set_xlabel("Time (hours)")
        self.fig.host.set_ylabel("Current ($\mu$A)")
        lines = [current_line]
        tkw = dict(size=4, width=1.5)
        self.fig.host.tick_params(axis='x', **tkw)

        if th:
            temp_averages = it.average_temp()
            temp_line, = self.fig.temp.plot(it.time, it.get_temperature(), color='b', alpha=0.4, label='Temperature, $T_{Av}$ = %s $\pm$ %s' % (temp_averages[0], temp_averages[1]))
            hum_line, = self.fig.hum.plot(it.time, it.get_humidity(), color='g', alpha=0.4, label='Humidity')

            self.fig.temp.yaxis.label.set_color(temp_line.get_color())
            self.fig.hum.yaxis.label.set_color(hum_line.get_color())
            #self.fig.hum.set_ylim([30, 50])
            #self.fig.temp.set_ylim([18, 22])
            self.fig.temp.set_ylabel("Temperature ($^\circ$C)")
            self.fig.hum.set_ylabel("Humidity (%)")
            self.fig.temp.tick_params(axis='y', colors=temp_line.get_color(), **tkw)
            self.fig.hum.tick_params(axis='y', colors=hum_line.get_color(), **tkw)

            lines.append(temp_line)
            lines.append(hum_line)

        if fits:
            fitting_data = Fitting.it_fits(it)
            maximum_line = self.fig.host.axhline(y=fitting_data[0], color = 'r', label = '$I_{max}$ = %s$\mu$A' % Fitting.round_sig(fitting_data[0],2))
            allowed_line = self.fig.host.axhline(y=fitting_data[2], color ='k', label = 'Allowed $I_{min}$ = %s$\mu$A, Result: %s' % (Fitting.round_sig(fitting_data[2],2), fitting_data[3]))
            minimum_line = self.fig.host.axhline(y=fitting_data[1], color = 'r', alpha= 0.6, label = '$I_{min}$ = %s$\mu$A' % Fitting.round_sig(fitting_data[1],2))
            lines.append(minimum_line)
            lines.append(maximum_line)
            lines.append(allowed_line)

        self.fig.host.legend(lines, [l.get_label() for l in lines])
        self.fig.suptitle(it.name)

    def plot_iv(self, th, fits, iv=Data()):

        current_line = self.fig.host.errorbar(x=iv.v_mean, y=iv.i_mean, yerr=iv.i_error, fmt='r.', label='Current')
        self.fig.host.set_xlabel("Voltage (V)")
        self.fig.host.set_ylabel("Current ($\mu$A)")
        lines = [current_line]
        tkw = dict(size=4, width=1.5)
        self.fig.host.tick_params(axis='x', **tkw)

        if th:
            temp_line, = self.fig.temp.plot(iv.v_mean, iv.temperature, color='b', alpha=0.4, label='Temperature')
            hum_line, = self.fig.hum.plot(iv.v_mean, iv.humidity, color='g', alpha=0.4, label='Humidity')

            self.fig.temp.yaxis.label.set_color(temp_line.get_color())
            self.fig.hum.yaxis.label.set_color(hum_line.get_color())
            #self.fig.hum.set_ylim([30, 50])
            #self.fig.temp.set_ylim([18, 22])
            self.fig.temp.set_ylabel("Temperature ($^\circ$C)")
            self.fig.hum.set_ylabel("Humidity (%)")
            self.fig.temp.tick_params(axis='y', colors=temp_line.get_color(), **tkw)
            self.fig.hum.tick_params(axis='y', colors=hum_line.get_color(), **tkw)

            lines.append(temp_line)
            lines.append(hum_line)

        if fits:
            bd_voltage = Fitting.breakdown_voltage(iv)[0]
            bd_statement = Fitting.breakdown_voltage(iv)[1]
            #print(bd_statement)
            if bd_voltage is not None:
                bd_line = self.fig.host.axvline(x=bd_voltage, color='r', linestyle='--', label='$V_{Breakdown}$ = %sV' % Fitting.round_sig(bd_voltage, 3))
                lines.append(bd_line)
            else:
                no_bd_line, = self.fig.host.plot([], [], ' ', label=bd_statement)
                lines.append(no_bd_line)

        self.fig.host.legend(lines, [l.get_label() for l in lines])
        self.fig.suptitle(iv.name)

    def plot_cv(self, th, fits, cv=Data()):
        #print('amw_3')
        capacitance_line = self.fig.host.errorbar(x=cv.v_mean, y=cv.inverse_c_squared, yerr=cv.inverse_c_squared_error, fmt='r.', label='Capacitance')
        self.fig.host.set_xlabel("Voltage (V)")
        self.fig.host.set_ylabel("$1/C^2$ ($1/pF^2$)")
        lines = [capacitance_line]
        tkw = dict(size=4, width=1.5)
        self.fig.host.tick_params(axis='x', **tkw)
        self.fig.host.set_ylim([0, max(cv.inverse_c_squared) * 1.1])

        if th:
            temp_line, = self.fig.temp.plot(cv.v_mean, cv.temperature, color='b', alpha=0.4, label='Temperature, $T_{Av}$ = %s $\pm$ %s' % (cv.average_temp()[0], cv.average_temp()[1]))
            hum_line, = self.fig.hum.plot(cv.v_mean, cv.humidity, color='g', alpha=0.4, label='Humidity, $H_{Av}$ = %s $\pm$ %s' % (cv.average_hum()[0], cv.average_hum()[1]))

            self.fig.temp.yaxis.label.set_color(temp_line.get_color())
            self.fig.hum.yaxis.label.set_color(hum_line.get_color())
            #self.fig.hum.set_ylim([30, 50])
            #self.fig.temp.set_ylim([18, 22])
            self.fig.temp.set_ylabel("Temperature ($^\circ$C)")
            self.fig.hum.set_ylabel("Humidity (%)")
            self.fig.temp.tick_params(axis='y', colors=temp_line.get_color(), **tkw)
            self.fig.hum.tick_params(axis='y', colors=hum_line.get_color(), **tkw)

            lines.append(temp_line)
            lines.append(hum_line)

        if fits:
            fit_data = Fitting.cv_fits(cv)
            self.fig.host.plot(cv.v_mean, fit_data[0], 'r')
            self.fig.host.plot(cv.v_mean, fit_data[1], 'r')
            full_depletion = self.fig.host.axvline(x=fit_data[2], linestyle='--', color='r',label='$V_{Full \: Depletion}$ = %s $\pm$ %sV' % (fit_data[2], fit_data[3]))
            lines.append(full_depletion)

        self.fig.host.legend(lines, [l.get_label() for l in lines])
        self.fig.suptitle(cv.name)

    def save_graph(self, output_folder, data):
        my_path = os.path.abspath(output_folder)
        my_type = data.type.upper()
        my_file = f'{self.fig.texts[0].get_text()}.png'
        if not os.path.isdir(my_path):
            os.mkdir(my_path)
        if not os.path.isdir(os.path.join(my_path, my_type)):
            os.mkdir(os.path.join(my_path, my_type))
        path = os.path.join(my_path, my_type, my_file)
        self.fig.savefig(path, bbox_inches='tight')

    def show_graph(self):
        #self.fig.tight_layout()
        plt.show(self)