import matplotlib.pyplot as plt
from Get_Data import Data
import Fitting
import os
from scipy import stats


class Plot:

    # Create a figure
    def __init__(self):
        self.fig = plt.figure()

    # Make and save the plots
    def plot_graph(self, output_folder, th, fits, data=Data()):
        # Create the axes
        self.add_axes(th=th)
        # Plot the data
        if data.type == 'it':
            self.plot_it(th, fits, data)
        elif data.type == 'cv':
            self.plot_cv(th, fits, data)
        elif data.type == 'iv':
            self.plot_iv(th, fits, data)
        # Save the graph
        self.save_graph(output_folder, data)


    # Hides the humidity x axis if using
    def make_patch_spines_invisible(ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)

    # Adds the axes to the figure
    def add_axes(self, th=False):
        # Adds the separate temperature and humidity axes
        if th:
            self.fig.host = self.fig.add_subplot()
            self.fig.subplots_adjust(right=0.75)

            self.fig.temp = self.fig.host.twinx()
            self.fig.hum = self.fig.host.twinx()

            self.fig.hum.spines["right"].set_position(("axes", 1.2))
            Plot.make_patch_spines_invisible(self.fig.hum)
            self.fig.hum.spines["right"].set_visible(True)
        # Just creates a standard graph
        else:
            self.fig.host = self.fig.add_subplot()

    # Plots It graphs
    def plot_it(self, th, fits, it=Data()):
        # Converts time from seconds to hours
        it.time_to_hours()

        """
        # A very rough method of trying to ignore anomalous points in the It data
        mean_current= sum(it.i_mean)/len(it.i_mean)
        mean_error = stats.tstd(it.i_mean)
        main_data_i = []
        main_data_t = []
        main_data_ierror =[]
        bad_data_i = []
        bad_data_t = []
        bad_data_ierror = []
        for i in range(len(it.i_mean)):
            if mean_current+(3 * mean_error) > it.i_mean[i] > mean_current - (3* mean_error):
                main_data_t.append(it.time[i])
                main_data_i.append(it.i_mean[i])
                main_data_ierror.append(it.i_error[i])
            else:
                bad_data_t.append(it.time[i])
                bad_data_i.append(it.i_mean[i])
                bad_data_ierror.append(it.i_error[i])
                
        current_line = self.fig.host.errorbar(x=main_data_t, y=main_data_i, yerr=main_data_ierror, fmt='r.',
                                              label='Current')
        current_line2 = self.fig.host.errorbar(x=bad_data_t, y=bad_data_i, yerr=bad_data_ierror, fmt='r.', alpha=0.5,
                                               label='Current')
        """

        # Plot the current data
        current_line = self.fig.host.errorbar(x=it.time, y=it.i_mean, yerr=it.i_error, fmt='r.', label='Current')
        # Set y axis range
        self.fig.host.set_ylim([min(it.i_mean) * 1.1, 0])
        # Label axis
        self.fig.host.set_xlabel("Time (hours)")
        self.fig.host.set_ylabel("Current ($\mu$A)")
        # List of all the lines
        lines = [current_line]
        # Line ticks
        tkw = dict(size=4, width=1.5)
        self.fig.host.tick_params(axis='x', **tkw)
        # If plotting temperature and humidity lines:
        if th:
            # Overall average temperature and humidity
            temp_averages = it.average_temp()
            hum_averages = it.average_hum()
            # Plot temperature and humidity lines
            temp_line, = self.fig.temp.plot(it.time, it.get_temperature(), color='b', alpha=0.4, label='Temperature, $T_{Av}$ = %s$^\circ$C' % temp_averages[0])
            hum_line, = self.fig.hum.plot(it.time, it.get_humidity(), color='g', alpha=0.4, label='Humidity, $H_{Av}$ = %s%%' % hum_averages[0])
            # Colour axis
            self.fig.temp.yaxis.label.set_color(temp_line.get_color())
            self.fig.hum.yaxis.label.set_color(hum_line.get_color())
            # Uncomment if you want to set the temperature and humidity axis range
            #self.fig.hum.set_ylim([30, 50])
            #self.fig.temp.set_ylim([18, 22])
            # Labels and tick sizes
            self.fig.temp.set_ylabel('Temperature ($^\circ$C)')
            self.fig.hum.set_ylabel('Humidity (%)')
            self.fig.temp.tick_params(axis='y', colors=temp_line.get_color(), **tkw)
            self.fig.hum.tick_params(axis='y', colors=hum_line.get_color(), **tkw)
            # Add to list of plotted lines
            lines.append(temp_line)
            lines.append(hum_line)
        # If testing the stability of the current
        if fits:
            fitting_data = Fitting.it_fits(it)
            maximum_line = self.fig.host.axhline(y=fitting_data[0], color='r', label='$I_{max}$ = %s$\mu$A' % Fitting.round_sig(fitting_data[0],2))
            allowed_line = self.fig.host.axhline(y=fitting_data[2], color='k', label='Allowed $I_{min}$ = %s$\mu$A, Result: %s' % (Fitting.round_sig(fitting_data[2],2), fitting_data[3]))
            minimum_line = self.fig.host.axhline(y=fitting_data[1], color='r', alpha=0.6, label='$I_{min}$ = %s$\mu$A' % Fitting.round_sig(fitting_data[1],2))
            # Add to list of plotted lines
            lines.append(minimum_line)
            lines.append(maximum_line)
            lines.append(allowed_line)

        # Create legend and title
        self.fig.host.legend(lines, [l.get_label() for l in lines])
        self.fig.suptitle(it.name)

    # Plot IV graphs
    def plot_iv(self, th, fits, iv=Data()):
        # Plot the current data
        current_line = self.fig.host.errorbar(x=iv.v_mean, y=iv.i_mean, yerr=iv.i_error, fmt='r.', label='Current')
        # Label axis
        self.fig.host.set_xlabel("Voltage (V)")
        self.fig.host.set_ylabel("Current ($\mu$A)")
        # List of plotted lines
        lines = [current_line]
        # Tick size
        tkw = dict(size=4, width=1.5)
        self.fig.host.tick_params(axis='x', **tkw)
        # If plotting temperature and humidity lines:
        if th:
            # Overall average temperature and humidity
            temp_averages = iv.average_temp()
            hum_averages = iv.average_hum()
            # Plot temperature and humidity
            temp_line, = self.fig.temp.plot(iv.v_mean, iv.temperature, color='b', alpha=0.4, label='Temperature, $T_{Av}$ = %s$^\circ$C' % temp_averages[0])
            hum_line, = self.fig.hum.plot(iv.v_mean, iv.humidity, color='g', alpha=0.4, label='Humidity, $H_{Av}$ = %s%%' % hum_averages[0])
            # Colour axis
            self.fig.temp.yaxis.label.set_color(temp_line.get_color())
            self.fig.hum.yaxis.label.set_color(hum_line.get_color())
            # Uncomment to constrain axis range
            #self.fig.hum.set_ylim([30, 50])
            #self.fig.temp.set_ylim([18, 22])
            # Label axis
            self.fig.temp.set_ylabel("Temperature ($^\circ$C)")
            self.fig.hum.set_ylabel("Humidity (%)")
            self.fig.temp.tick_params(axis='y', colors=temp_line.get_color(), **tkw)
            self.fig.hum.tick_params(axis='y', colors=hum_line.get_color(), **tkw)
            # Add to list of lines
            lines.append(temp_line)
            lines.append(hum_line)
        # If finding the breakdown voltage:
        if fits:
            bd_voltage = Fitting.breakdown_voltage(iv)[0]
            bd_statement = Fitting.breakdown_voltage(iv)[1]
            #print(bd_statement)
            # Plot a vertical line at breakdown voltage
            if bd_voltage is not None:
                bd_line = self.fig.host.axvline(x=bd_voltage, color='r', linestyle='--', label='$V_{Breakdown}$ = %sV' % Fitting.round_sig(bd_voltage, 3))
                lines.append(bd_line)
            else:
                no_bd_line, = self.fig.host.plot([], [], ' ', label=bd_statement)
                lines.append(no_bd_line)
        # Create legend and title
        self.fig.host.legend(lines, [l.get_label() for l in lines])
        self.fig.suptitle(iv.name)

    # PLot CV graphs
    def plot_cv(self, th, fits, cv=Data()):
        #print('amw_3')
        # Plot capacitance data
        capacitance_line = self.fig.host.errorbar(x=cv.v_mean, y=cv.inverse_c_squared, yerr=cv.inverse_c_squared_error, fmt='r.', label='Capacitance')
        # Label axis
        self.fig.host.set_xlabel("Voltage (V)")
        self.fig.host.set_ylabel("$1/C^2$ ($1/pF^2$)")
        # List of plotted lines
        lines = [capacitance_line]
        # Tick size and y axis limit
        tkw = dict(size=4, width=1.5)
        self.fig.host.tick_params(axis='x', **tkw)
        self.fig.host.set_ylim([0, max(cv.inverse_c_squared) * 1.1])
        # If plotting temperature and humidity:
        if th:
            # Overall average temperature and humidity
            temp_averages = cv.average_temp()
            hum_averages = cv.average_hum()
            # Plot temperature and humidity
            temp_line, = self.fig.temp.plot(cv.v_mean, cv.temperature, color='b', alpha=0.4, label='Temperature, $T_{Av}$ = %s$^\circ$C' % temp_averages[0])
            hum_line, = self.fig.hum.plot(cv.v_mean, cv.humidity, color='g', alpha=0.4, label='Humidity, $H_{Av}$ = %s%%' % hum_averages[0])
            # Colour axis
            self.fig.temp.yaxis.label.set_color(temp_line.get_color())
            self.fig.hum.yaxis.label.set_color(hum_line.get_color())
            # Uncomment to constrain axis range
            #self.fig.hum.set_ylim([30, 50])
            #self.fig.temp.set_ylim([18, 22])
            # Label axis and tick parameters
            self.fig.temp.set_ylabel('Temperature ($^\circ$C)')
            self.fig.hum.set_ylabel('Humidity (%)')
            self.fig.temp.tick_params(axis='y', colors=temp_line.get_color(), **tkw)
            self.fig.hum.tick_params(axis='y', colors=hum_line.get_color(), **tkw)
            # Add to list of lines
            lines.append(temp_line)
            lines.append(hum_line)
        # if finding the depletion voltage
        if fits:
            # Get data
            fit_data = Fitting.cv_fits(cv)
            # Plot two linear lines
            self.fig.host.plot(cv.v_mean, fit_data[0], 'r')
            self.fig.host.plot(cv.v_mean, fit_data[1], 'r')
            # Plot line at full depletion
            full_depletion = self.fig.host.axvline(x=fit_data[2], linestyle='--', color='r',label='$V_{Full \: Depletion}$ = %s $\pm$ %sV' % (fit_data[2], fit_data[3]))
            # Add to list of lines
            lines.append(full_depletion)
        # Create legend and title
        self.fig.host.legend(lines, [l.get_label() for l in lines])
        self.fig.suptitle(cv.name)

    # Save the graph
    def save_graph(self, output_folder, data):
        # Path to where to save the data
        my_path = os.path.abspath(output_folder)
        # Type of graph
        my_type = data.type.upper()
        # Name of the file
        my_file = f'{self.fig.texts[0].get_text()}.png'
        # Check if these folder exist, if not, create them
        if not os.path.isdir(my_path):
            os.mkdir(my_path)
        if not os.path.isdir(os.path.join(my_path, my_type)):
            os.mkdir(os.path.join(my_path, my_type))
        # Complete path
        path = os.path.join(my_path, my_type, my_file)
        # Save
        self.fig.savefig(path, bbox_inches='tight')

    # Show this graph - this doesnt work very well
    def show_graph(self):
        #self.fig.tight_layout()
        plt.show(self)
