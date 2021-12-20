
# load required python packages
import matplotlib.pyplot as plt
import numpy as np
import netCDF4 as nc
import argparse
import configparser
import sys
import matplotlib as mpl
from pathlib import Path

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

    args = parser.parse_args()

#####################

# B) Read config file

#####################

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
    height = config.getfloat('var','height')

#############

# C) Plotting

#############

    # load data
    with nc.Dataset(input_file) as ncf:
        time = ncf.variables['time'][:]
        var = ncf.variables[var_name][:,height,:]
    time = time.astype('str')
    # Calculate mean and standard deviation
    var_mean = var.mean(axis=1)
    var_std = var_mean.std(axis=0)

    # plot settings
    f, axes = plt.subplots(1,1)
    ax = axes
    ax.fill_between(time, var_mean-var_std, var_mean+var_std, color='#a6bddb')
    h = ax.plot(time, var_mean, lw=2)
    if (config.has_section('plot')):
        if (config.has_option('plot','label_var')):
            label_var = config.get('plot','label_var')
            ax.set_ylabel(label_var)
        if (config.has_option('plot','label_time')):
            label_time = config.get('plot','label_time')
            ax.set_xlabel(label_time)
        if (config.has_option('plot','title')):
            title = config.get('plot','title')
            ax.set_title(title, fontsize=14)
        if (config.has_option('plot','ylim')):
            ylim = config.get('plot','ylim')
            ylim = ylim.split(', ')
            ylim = list(map(float,ylim))
            plt.ylim(ylim)
        if (config.has_option('plot','xlim')):
            xlim = config.get('plot','xlim')
            xlim = xlim.split(', ')
            xlim = list(map(float,xlim))
            plt.xlim(xlim)
    ax.axhline(0, color='0.1', lw=0.5)
    plt.xticks(rotation=45)
    
    # save figure
    output_dir = Path(args.output_dir)
    output_file = Path(output_dir,args.output_file)
    output_dir.mkdir(parents=True,exist_ok=True)
    print("The output is saved as " + str(output_file))
    plt.savefig(output_file)
