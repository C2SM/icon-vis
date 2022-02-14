
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
import psyplot.project as psy
import six


def get_several_input(sect,opt,f=False):
    var = config.get(sect,opt)
    var = var.replace(', ',',')
    var = var.split(',')
    if f:
        var = list(map(float,var))
    return var

def ind_from_latlon(lats, lons, lat, lon, verbose=False):
    """Find the nearest neighbouring index to given location.
    Args:
        lats (2d array):            Latitude grid
        lons (2d array):            Longitude grid
        lat (float):                Latitude of location
        lon (float):                Longitude of location
        verbose (bool, optional):   Print information. Defaults to False.
    Returns:
        int     Index of nearest grid point.
    """
    dist = [
        np.sqrt((lats[i] - lat) ** 2 + (lons[i] - lon) ** 2) for i in range(len(lats))
    ]
    ind = np.where(dist == np.min(dist))[0][0]
    if verbose:
        print(f"Closest ind: {ind}")
        print(f" Given lat: {lat:.3f} vs found lat: {lats[ind]:.3f}")
        print(f" Given lot: {lon:.3f} vs found lon: {lons[ind]:.3f}")
    return ind

def add_encoding(obj):
    obj.encoding['coordinates'] = 'clat clon'


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
                'var, time (opt): index of time variable. Default 0.\n'+\
                'var, grid_file (req if file is missing grid-information): path to grid file\n'+\
                'plot, xlabel/ylabel (opt): x and y labels\n'+\
                'plot, title (opt): title of plot\n'+\
                'plot, xlim/ylim (opt): lower and upper limit of x or y axis (two numbers needed)\n'+\
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
    var_name = config.get('var','name')

#############

# C) Plotting

#############

    # load data
    if config.has_option('var','grid_file'):
        grid_file = config.get('var','grid_file')
        grid_ds = psy.open_dataset(grid_file)
        icon_ds = psy.open_dataset(input_file).squeeze()
        data = icon_ds.rename({"ncells":"cell"}).merge(grid_ds)
        for k, v in six.iteritems(data.data_vars):
            add_encoding(v)
    else:
        data = psy.open_dataset(input_file)

    var_field = getattr(data,var_name)
    values = var_field.values

    if config.has_option('var','time'):
        time = config.getint('var','time')
    else:
        time = 0

    var_dims = var_field.dims
    height_ind = [i for i, s in enumerate(var_dims) if 'height' in s]
    if bool(height_ind):
        height_dim = var_dims[height_ind[0]]
        height = getattr(data,height_dim).values[:]
    else:
        sys.exit("No altitiude information is given for " + var_name +".")

    if 'time' in var_dims:
        var = values[time,:,:]
        height_dim = var_field.dims[1]
    else:
        var = values
        height_dim = var_field.dims[0]
    
    if (config.has_section('coord')):
        lat = config.getfloat('coord','lat')
        lon = config.getfloat('coord','lon')
        # convert from radians to degrees
        lats = np.rad2deg(data.clat.values[:])
        lons = np.rad2deg(data.clon.values[:])
        # Get cell index of closes cell
        ind = ind_from_latlon(lats,lons,lat,lon,verbose=True)
        var = var[:,ind]
    else:
        var = var.mean(axis=1)

    # plot settings
    f, axes = plt.subplots(1,1)
    ax = axes
    h = ax.plot(var, height, lw=2)
    if (config.has_section('plot')):
        if (config.has_option('plot','xlabel')):
            xlabel = config.get('plot','xlabel')
            ax.set_xlabel(xlabel)
        if (config.has_option('plot','ylabel')):
            ylabel = config.get('plot','ylabel')
            ax.set_ylabel(ylabel)
        if (config.has_option('plot','title')):
            title = config.get('plot','title')
            ax.set_title(title, fontsize=14)
        if (config.has_option('plot','ylim')):
            ylim = get_several_input('plot','ylim',f=True)
            plt.ylim(ylim)
        if (config.has_option('plot','xlim')):
            xlim = get_several_input('plot','xlim',f=True)
            plt.xlim(xlim)
    ax.axhline(0, color='0.1', lw=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout() 
    # save figure
    output_dir = Path(args.output_dir)
    output_file = Path(output_dir,args.output_file)
    output_dir.mkdir(parents=True,exist_ok=True)
    print("The output is saved as " + str(output_file))
    plt.savefig(output_file)
