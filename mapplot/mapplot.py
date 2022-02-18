# 2-dimensional mapplot of surface height
# Date: October 14, 2021
# Author: Stephanie Westerhuis
# Adapted: Nadja Omanovic
# Adapted: Annika Lauber
# use with config_mapplot.ini

# load required python packages
import matplotlib.pyplot as plt
import matplotlib as mpl
import cmcrameri.cm as cmc
import cartopy.feature as cf
import configparser
from pathlib import Path
import psyplot.project as psy
import argparse
import sys
import six
data_dir = Path(Path.cwd().parent,'python_modules')
sys.path.insert(1,str(data_dir))
from config import get_several_input
from grid import check_grid_information,add_grid_information


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
                            default = 'mapplot_output.png')
    parser.add_argument('-co', action = 'store_true',\
                            help = 'get config options')
    args = parser.parse_args()

#####################

# B) Read config file

#####################

    if args.co:
        print('map, lonmin/lonmax/latmin/latmax (req): values for map extension\n'+\
                'map, projection (req): projection to draw on (e.g., robin)\n'+\
                'map, add_grid (req): set true for adding grid with lat and lon labels\n'+\
                'var, name (req): name of the variable as in the nc file\n'+\
                'var, title (req): title of plot\n'+\
                'var, varlim (opt): lower and upper limit of color scale\n'+\
                'var, grid_file (req if file is missing grid-information): path to grid file\n'+\
                'var, time (opt): index/es of time variable (creates a range of plots between two given indexes divided by comma)\n'+\
                'coord, name (opt): add markers at certain locations (several inputs possible)\n'+\
                'coord, lon/lat (req if coord, name): lon and lat of the locations\n'+\
                'coord, marker (opt): marker specifications for all locations\n'+\
                'coord, marker_size (opt): marker sizes for all locations\n'+\
                'coord, col (opt): colors of all markers for all locations')
        sys.exit()


    config = configparser.ConfigParser(inline_comment_prefixes='#')
    try:
        config.read(args.config_path)
    except Exception as e:
        sys.exit("Please provide a valid config file")
    
    # Check if input file exists
    input_file = Path(args.input_file)
    if (not input_file.is_file()):
        sys.exit(args.input_file + " is not a valid file name")

    # map appearance
    lonmin = config.getfloat('map','lonmin')
    lonmax = config.getfloat('map','lonmax')
    latmin = config.getfloat('map','latmin')
    latmax = config.getfloat('map','latmax')
    projection = config.get('map','projection')
    add_grid = config.getboolean('map','add_grid')

    # variable and related things
    var_name = config.get('var','name')
    title = config.get('var','title')

#############

# C) Plotting

#############

    # psyplot settings
    psy.rcParams["plotter.maps.xgrid"] = False
    psy.rcParams["plotter.maps.ygrid"] = False
    psy.rcParams["plotter.plot2d.cmap"] = cmc.nuuk  # 'cividis'
    mpl.rcParams['figure.figsize'] = [6., 6.]

    if check_grid_information(input_file):
        ds = psy.open_dataset(input_file)
    elif config.has_option('var','grid_file'):
        grid_file = config.get('var','grid_file')
        ds = add_grid_information(input_file,grid_file)
    else:
        sys.exit('The file '+str(input_file)+\
                ' is missing the grid information. Please provide a grid file in the config.')

    if config.has_option('var','time'):
        t = get_several_input(config,'var','time',i=True)
    else:
        t[0] = 0
    if len(t) == 1:
        end_t = t[0]+1
    else:
        end_t = t[1]+1

    for i in range(t[0],end_t):
        # create psyplot instance
        if config.has_option('var','varlim'):
            varlim = get_several_input(config,'var','varlim',f=True)
            pp = psy.plot.mapplot(ds,
                name = var_name,
                t = i,
                projection = projection,
                bounds = {'method': 'minmax', 'vmin':varlim[0], 'vmax':varlim[1]},
                map_extent = [lonmin, lonmax, latmin, latmax],
                title = title,
                enable_post = True,
                xgrid = add_grid,
                ygrid = add_grid)
        else:
            pp = psy.plot.mapplot(ds,
                name = var_name,
                t = i,
                projection = projection,
                map_extent = [lonmin, lonmax, latmin, latmax],
                title = title,
                enable_post = True,
                xgrid = add_grid,
                ygrid = add_grid)

        # access matplotlib axes
        ax = pp.plotters[0].ax

        # add borders with cartopy
        resol = '10m'
        lakes = cf.NaturalEarthFeature(category='physical', name='lakes', scale=resol, edgecolor='k', facecolor='k')
        ax.add_feature(cf.BORDERS)
        ax.add_feature(lakes)

        # go to matplotlib level
        fig = plt.gcf()

        if config.has_section('coord'):
            name_coord = get_several_input(config,'coord','name')
            len_coord = len(name_coord)
            lon_coord = get_several_input(config,'coord','lon',f=True)
            lat_coord = get_several_input(config,'coord','lat',f=True)
            llon = lonmax-lonmin
            llat = latmax-latmin
            if config.has_option('coord','marker'):
                m = get_several_input(config,'coord','marker')
            else:
                m = ['*']*len_coord
            if config.has_option('coord','col'):
                c = get_several_input(config,'coord','col')
            else:
                c = ['r']*len_coord
            if config.has_option('coord','marker_size'):
                ms = get_several_input(config,'coord','marker_size',f=True)
            else:
                ms = [10]*len_coord
            for i in range(0,len_coord):
                pos_lon = (lon_coord[i]-lonmin)/llon
                pos_lat = (lat_coord[i]-latmin)/llat
                fig.axes[0].plot(pos_lon, pos_lat, c[i], marker=m[i], markersize=ms[i], transform=fig.axes[0].transAxes)
                fig.axes[0].text(pos_lon+llon*0.003, pos_lat+llat*0.003, name_coord[i], transform=fig.axes[0].transAxes)

        # save figure
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True,exist_ok=True)
        if (len(t) > 1):
            name_file = args.output_file + '_' + str(i)
        else:
            name_file = args.output_file
        output_file = Path(output_dir,name_file)
        print("The output is saved as " + str(output_file))
        plt.savefig(output_file)
