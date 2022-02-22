# load required python packages
import matplotlib.pyplot as plt
import numpy as np
import argparse
import configparser
import sys
from pathlib import Path
import matplotlib.dates as mdates
import psyplot.project as psy
import six

data_dir = Path(Path(__file__).resolve().parents[1], 'modules')
sys.path.insert(1, str(data_dir))
from config import get_several_input
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

    # B) Read config file

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

    # read configuration
    config = configparser.ConfigParser(inline_comment_prefixes='#')
    try:
        config.read(args.config_path)
    except Exception as e:
        sys.exit("Please provid a valid config file")

    # Check if input file exists
    input_file = Path(args.input_file)
    if (not input_file.is_file()):
        sys.exit(args.input_file + " is not a valid file name")

    # variable and related things
    var_name = config.get('var', 'name')
    if config.has_option('var', 'height'):
        height = config.getint('var', 'height')
    else:
        height = 0

#############

# C) Plotting

#############

# load data
    if check_grid_information(input_file):
        data = psy.open_dataset(input_file)
    elif config.has_option('var', 'grid_file'):
        grid_file = config.get('var', 'grid_file')
        data = add_grid_information(input_file, grid_file)
    else:
        sys.exit('The file '+str(input_file)+\
                ' is missing the grid information. Please provide a grid file in the config.')

    var_field = getattr(data, var_name)
    values = var_field.values

    if 'time' not in var_field.dims:
        sys.exit("Only one timestep given. No timeseries can be plotted.")
    else:
        time = data.time.values[:]

    if 'height' in var_field.dims[1]:
        var = values[:, height, :]
    else:
        var = values

    if (config.has_section('coord')):
        lat = config.getfloat('coord', 'lat')
        lon = config.getfloat('coord', 'lon')
        # convert from radians to degrees
        lats = np.rad2deg(data.clat.values[:])
        lons = np.rad2deg(data.clon.values[:])
        # Get cell index of closes cell
        ind = ind_from_latlon(lats, lons, lat, lon, verbose=True)
        var = var[:, ind]
    else:
        var = var.mean(axis=1)

    # plot settings
    f, axes = plt.subplots(1, 1)
    ax = axes
    # plot uncertainty
    if config.has_option('var', 'unc'):
        unc = config.get('var', 'unc')
        if (unc == 'std'):
            var_std = var.std(axis=0)
            ax.fill_between(time,
                            var - var_std,
                            var + var_std,
                            color='#a6bddb')

    h = ax.plot(time, var, lw=2)
    date_format = '%Y-%m-%d %H:%M'
    if (config.has_section('plot')):
        if (config.has_option('plot', 'ylabel')):
            ylabel = config.get('plot', 'ylabel')
            ax.set_ylabel(ylabel)
        if (config.has_option('plot', 'xlabel')):
            xlabel = config.get('plot', 'xlabel')
            ax.set_xlabel(xlabel)
        if (config.has_option('plot', 'title')):
            title = config.get('plot', 'title')
            ax.set_title(title, fontsize=14)
        if (config.has_option('plot', 'ylim')):
            ylim = get_several_input(config, 'plot', 'ylim', f=True)
            plt.ylim(ylim)
        if (config.has_option('plot', 'xlim')):
            xlim = get_several_input(config, 'plot', 'xlim', f=True)
            plt.xlim(xlim)
        if (config.has_option('plot', 'date_format')):
            date_format = config.get('plot', 'date_format')
    myFmt = mdates.DateFormatter(date_format)
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
