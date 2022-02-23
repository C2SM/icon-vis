# load required python packages
import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys
from pathlib import Path
import matplotlib.dates as mdates
import psyplot.project as psy
import six

data_dir = Path(Path(__file__).resolve().parents[1], 'modules')
sys.path.insert(1, str(data_dir))
from config import read_config
from utils import ind_from_latlon
from grid import add_grid_information, check_grid_information

if __name__ == "__main__":

    ####################

    # A) Parsing arguments

    ####################

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', dest = 'config_path',\
                            help = 'path to config file')
    parser.add_argument('--infile', '-i', dest = 'input_file',\
                            help = 'path to input file',\
                            default='')
    parser.add_argument('--outdir', '-d', dest = 'output_dir',\
                            help = 'output directory',\
                            default=Path.cwd())
    parser.add_argument('--outfile', '-o', dest = 'output_file',\
                            help = 'name of output file',\
                            default = 'timeseries_output.png')
    parser.add_argument('-co', action = 'store_true',\
                            help = 'get config options')
    args = parser.parse_args()

    #####################

    # B) Read config file or show available options

    #####################

    if args.co:
        print('var, name (req): name of variable as in nc file\n'+\
                'var, height (opt): index of dimension height from variable (default 0)\n'+\
                'var, unc (opt): add uncertainty to plot (only available option std=standard deviation)\n'+\
                'var, grid_file (req if file is missing grid-information): path to grid file\n'+\
                'plot, xlabel/ylabel (opt): x and y labels\n'+\
                'plot, title (opt): title of plot\n'+\
                'plot, xlim/ylim (opt): lower and upper limit of x or y axis (two numbers needed)\n'+\
                'plot, data_format (opt): date format (needs two % after each other)\n'+\
                'coord, lon/lat (req if section coord): height profile of closest grid cell point (mean over whole map if not given)')
        sys.exit()

    # read config file
    var, _, coord, plot = read_config(args.config_path)

    #############

    # C) Load data

    #############

    # Check if input file exists
    input_file = Path(args.input_file)
    if (not input_file.is_file()):
        sys.exit(args.input_file + " is not a valid file name")

    # load data
    if check_grid_information(input_file):
        data = psy.open_dataset(input_file)
    elif 'grid_file' in var.keys():
        data = add_grid_information(input_file, var['grid_file'])
    else:
        sys.exit('The file '+str(input_file)+\
                ' is missing the grid information. Please provide a grid file in the config.')

    # variable and related things
    var_field = getattr(data, var['name'])
    var_dims = var_field.dims
    values = var_field.values

    # Check if time exists as dimension
    if 'time' not in var_dims:
        sys.exit("Only one timestep given. No timeseries can be plotted.")
    else:
        time = data.time.values[:]

    # Check if height exists as dimension
    if 'height' in var_field.dims[1]:
        values_red = values[:, var['height'][0], :]
    else:
        values_red = values

    # Check if coordinates are given
    if coord:
        # convert from radians to degrees
        lats = np.rad2deg(data.clat.values[:])
        lons = np.rad2deg(data.clon.values[:])
        # Get cell index of closes cell
        ind = ind_from_latlon(lats,
                              lons,
                              coord['lat'][0],
                              coord['lon'][0],
                              verbose=True)
        values_red = values_red[:, ind]
    else:
        values_red = values_red.mean(axis=1)

    #############

    # C) Plotting

    #############

    # plot settings
    f, axes = plt.subplots(1, 1)
    ax = axes
    # plot uncertainty
    if 'unc' in var.keys():
        if (var['unc'] == 'std'):
            var_std = values_red.std(axis=0)
            ax.fill_between(time,
                            values_red - var_std,
                            values_red + var_std,
                            color='#a6bddb')

    h = ax.plot(time, values_red, lw=2)
    if 'xlabel' in plot.keys():
        ax.set_xlabel(plot['xlabel'])
    if 'ylabel' in plot.keys():
        ax.set_ylabel(plot['ylabel'])
    if 'title' in plot.keys():
        ax.set_title(plot['title'])
    if 'ylim' in plot.keys():
        plt.ylim(plot['ylim'])
    if 'xlim' in plot.keys():
        plt.xlim(plot['xlim'])

    myFmt = mdates.DateFormatter(plot['date_format'])
    ax.xaxis.set_major_formatter(myFmt)
    ax.axhline(0, color='0.1', lw=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    # save figure
    output_dir = Path(args.output_dir)
    output_file = Path(output_dir, args.output_file)
    output_dir.mkdir(parents=True, exist_ok=True)
    print("The output is saved as " + str(output_file))
    plt.savefig(output_file)
