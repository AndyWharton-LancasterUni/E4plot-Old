from Get_Data import Data
from Plotting import Plot
import argparse
import os
import glob


parser = argparse.ArgumentParser()
parser.add_argument('file_directory', help='path to the folder containing the data')
parser.add_argument('-o', '--output_directory', help='folder in which to save the data', default=' ', type=str)
parser.add_argument('-iv', '--plot_iv', help='plot all iv files, default: yes', default=True)
parser.add_argument('-cv', '--plot_cv', help='plot all cv files, default: yes', default=True)
parser.add_argument('-it', '--plot_it', help='plot all it files, default: yes', default=True)
parser.add_argument('-it_th', '--plot_itth', help='plot temperature and humidity for it curves', default=True)
parser.add_argument('-cv_th', '--plot_cvth', help='plot temperature and humidity for cv curves', default=True)
parser.add_argument('-iv_th', '--plot_ivth', help='plot temperature and humidity for iv curves', default=True)
parser.add_argument('-it_f', '--plot_itf', help='test for greater than 20 percent variations in the data', default=True)
parser.add_argument('-cv_f', '--plot_cvf', help='find and plot the depletion voltage', default=True)
parser.add_argument('-iv_f', '--plot_ivf', help='find and plot the breakdown voltage', default=True)
#parser.add_argument('-it_g', '--plot_itg', help='plot all it curves on one graph (requires -it_th to be False)', default=False)
#parser.add_argument('-cv_g', '--plot_cvg', help='plot all cv curves on one graph (requires -cv_th to be False)', default=False)
#parser.add_argument('-iv_g', '--plot_ivg', help='plot all iv curves on one graph (requires -it_th to be False)', default=False)
parser.add_argument('-av', '--choose_average', help='calculate current and capacitance averages using median (default is mean)', default='mean', type=str)


# Method to convert a string input into the correct boolean
def input_boolean(argument):
    if argument is not True:
        if argument.lower() == ('1' or 'true' or 'y'):
            #print('returning true')
            return True
        else:
            #print('returning false')
            return False
    else:
        return True


def main():
    print('Running!')
    # Read in arguments from the command line
    args = parser.parse_args()
    # Folder containing the data
    input_directory = args.file_directory
    # Folder to which the graphs should be saved
    if args.output_directory == ' ':
        output_directory = args.file_directory
    else:
        output_directory = args.output_directory

    # Assign variable with inputs from the command line
    plot_iv = input_boolean(args.plot_iv)
    plot_cv = input_boolean(args.plot_cv)
    plot_it = input_boolean(args.plot_it)
    plot_ivth = input_boolean(args.plot_ivth)
    plot_cvth = input_boolean(args.plot_cvth)
    plot_itth = input_boolean(args.plot_itth)
    plot_ivf = input_boolean(args.plot_ivf)
    plot_cvf = input_boolean(args.plot_cvf)
    plot_itf = input_boolean(args.plot_itf)
    #plot_ivg = input_boolean(args.plot_ivg)
    #plot_cvg = input_boolean(args.plot_cvg)
    #plot_itg = input_boolean(args.plot_itg)
    average_type = args.choose_average

    # Print inputs
    print('Input Directory: ' + input_directory)
    print('Output Directory: ' + output_directory)
    print(f'Plot CV Graphs: {plot_cv}')
    print(f'Plot IV Graphs: {plot_iv}')
    print(f'Plot It Graphs: {plot_it}')
    print(f'Plot CV Graphs with temperature and humidity: {plot_cvth}')
    print(f'Plot IV Graphs with temperature and humidity: {plot_ivth}')
    print(f'Plot It Graphs with temperature and humidity: {plot_itth}')
    print(f'Plot IV Graphs with fits: {plot_ivf}')
    print(f'Plot It Graphs with fits: {plot_itf}')
    print('Calculate averages using ' + average_type)

    # List of data files
    files = []
    #print(os.listdir(input_directory))
    folder = os.listdir(input_directory)
    # Struggled to get the code below to work
    """
    for Input in args.file_directory:
        print("\tInput, ", Input)
        OSInputs = sorted(glob.glob(Input+'/*.txt'))
        print(OSInputs)
        for OSInput in OSInputs:
            if os.path.isfile(OSInput) and OSInput.endswith('.txt') and 'short' not in OSInput:
                files.append(OSInput)
                print("\t\t" + OSInput)
    """
    # Fill files list
    for filename in folder:
        if os.path.isfile(os.path.join(input_directory, filename)) and filename.endswith('.txt') and 'short' not in filename:
            files.append(os.path.join(input_directory, filename))
        else:
            continue

    file_data = {}
    #print(files)

    # Create a dictionary with all the data files and the corresponding data object
    for i in range(len(files)):
        data = Data()
        data.extract_data(files[i], average_type)
        file_data[files[i]] = data

    """
    for f in file_data.values():
        print(f.v_mean)
        continue
    """

    # Separate the data into IV, CV and It
    iv_data = {}
    cv_data = {}
    it_data = {}
    for f1, f2 in file_data.items():
        if f2.type == 'iv':
            iv_data[f1] = f2
        elif f2.type == 'cv':
            cv_data[f1] = f2
        elif f2.type == 'it':
            it_data[f1] = f2

    # Plot all IV files
    if plot_iv:
        print('Plotting IV Graphs')
        for f1, f2 in iv_data.items():
            graph = Plot()
            graph.plot_graph(output_directory, plot_ivth, plot_ivf, f2)
    # Plot all CV files
    if plot_cv:
        print('Plotting CV Graphs')
        for f1, f2 in cv_data.items():
            graph = Plot()
            graph.plot_graph(output_directory, plot_cvth, plot_cvf, f2)
    # Plot all It files
    if plot_it:
        print('Plotting It Graphs')
        for f1, f2 in it_data.items():
            graph = Plot()
            graph.plot_graph(output_directory, plot_itth, plot_itf, f2)

    #print(file_data)


if __name__ == '__main__':
    main()

