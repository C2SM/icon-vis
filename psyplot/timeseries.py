
# load required python packages
import matplotlib.pyplot as plt
import numpy as np
import netCDF4 as nc
import argparse
import configparser
import sys
import matplotlib as mpl
from pathlib import Path
import matplotlib.dates as mdates
from datetime import datetime
import cftime as cftime


def get_several_input(sect,opt,f=False):
    var = config.get(sect,opt)
    var = var.replace(', ',',')
    var = var.split(',')
    if f:
        var = list(map(float,var))
    return var


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
                'var, unc (opt): add ucnertainty to plot (only available option std=standard deviation)\n'+\
                'plot, xlabel/ylabel (opt): x and y labels\n'+\
                'plot, title (opt): title of plot\n'+\
                'plot, xlim/ylim (opt): lower and upper limit of x or y axis (two numbers needed)\n'+\
                'plot, data_format (opt): date format (needs two % after each other)')
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
    var_name = config.get('var','name')
    if config.has_option('var','height'):
        height = config.getfloat('var','height')
    else:
        height = 0

#############

# C) Plotting

#############

    # load data
    with nc.Dataset(input_file) as ncf:
        time_var = ncf.variables['time'][:]
        units = ncf.variables['time'].units
        if 'since' not in units:
            timestep, _, t_fmt_str = units.split(' ')
            nctime_str = ["%8.6f" % x for x in time_var]
            ncdate = ( datetime.strptime(x, t_fmt_str) for x in nctime_str)
            time = [ x for x in ncdate]
        else:
            time = cftime.num2pydate(time_var,units)
        if ('height' in ncf.variables[var_name].dimensions):
            var = ncf.variables[var_name][:,height,:]
        else:
            var = ncf.variables[var_name][:,:]
    # Calculate mean and standard deviation
    var_mean = var.mean(axis=1)

    # plot settings
    f, axes = plt.subplots(1,1)
    ax = axes
    # plot uncertainty
    if config.has_option('var','unc'):
        unc = config.get('var','unc')
        if (unc == 'std'):
            var_std = var_mean.std(axis=0)
            ax.fill_between(time, var_mean-var_std, var_mean+var_std, color='#a6bddb')

    h = ax.plot(time, var_mean, lw=2)
    date_format = '%Y-%m-%d %H:%M'
    if (config.has_section('plot')):
        if (config.has_option('plot','ylabel')):
            ylabel = config.get('plot','ylabel')
            ax.set_ylabel(ylabel)
        if (config.has_option('plot','xlabel')):
            xlabel = config.get('plot','xlabel')
            ax.set_xlabel(xlabel)
        if (config.has_option('plot','title')):
            title = config.get('plot','title')
            ax.set_title(title, fontsize=14)
        if (config.has_option('plot','ylim')):
            ylim = get_several_input('plot','ylim',f=True)
            plt.ylim(ylim)
        if (config.has_option('plot','xlim')):
            xlim = get_several_input('plot','xlim',f=True)
            plt.xlim(xlim)
        if (config.has_option('plot','date_format')):
            date_format = config.get('plot','date_format')
    myFmt = mdates.DateFormatter(date_format)
    ax.xaxis.set_major_formatter(myFmt)
    ax.axhline(0, color='0.1', lw=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout() 
    # save figure
    output_dir = Path(args.output_dir)
    output_file = Path(output_dir,args.output_file)
    output_dir.mkdir(parents=True,exist_ok=True)
    print("The output is saved as " + str(output_file))
    plt.savefig(output_file)
