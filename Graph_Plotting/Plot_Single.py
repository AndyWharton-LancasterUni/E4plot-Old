from Get_Data import Data
from Plotting import Plot
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('file_path', help='path to the file containing the data')
parser.add_argument('-n', '--name', help='name of the graph', default='', type=str)
parser.add_argument('-o', '--output_directory', help='folder in which to save the data', default=' ', type=str)
parser.add_argument('-t', '--plot_type', help='plot cv, iv or it', type=str, default='')
parser.add_argument('-th', '--plot_temp_and_hum', help='include temperature and humidity', default=True)
parser.add_argument('-f', '--plot_fits', help='plot the appropriate fit', default=True)
parser.add_argument('-av', '--choose_average', help='calculate the average using the median or mean', type=str, default='mean')
parser.add_argument('-r', '--remove_anomolous', help='remove an anomolous point', type =int, nargs='+', default= None)


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
    # File to be plotted
    input_path = args.file_path
    path, file = os.path.split(input_path)
    # Folder to which the graph should be saved
    if args.output_directory == ' ':
        output_directory = path
    else:
        output_directory = args.output_directory

    # Assign variable with inputs from the command line
    name = args.name
    plot_type = args.plot_type
    plot_th = input_boolean(args.plot_temp_and_hum)
    plot_fit = input_boolean(args.plot_fits)
    average = args.choose_average
    remove = args.remove_anomolous

    # Extract the data
    data = Data()
    data.name = name
    data.type = plot_type
    data.extract_data(input_path, average)

    if remove is not None:
        for i in range(len(remove)):
            data.remove_anomalies(i)

    # Plot the graph
    plot = Plot()
    plot.plot_graph(output_directory, plot_th, plot_fit, data)


if __name__ == '__main__':
    main()
