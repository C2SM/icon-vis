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
import cartopy.crs as ccrs
import configparser
from pathlib import Path
import psyplot.project as psy
import argparse
import sys

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

    args = parser.parse_args()

#####################

# B) Read config file

#####################

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
    vmin = config.getfloat('map','vmin')
    vmax = config.getfloat('map','vmax')
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

    # create psyplot instance
    pp = psy.plot.mapplot(args.input_file,
    name = var_name,
    projection = projection,
    bounds = {'method': 'minmax', 'vmin':vmin, 'vmax':vmax}, 
    map_extent = [lonmin, lonmax, latmin, latmax],
    title=title + ' on %Y-%m-%d %H:%M',
    enable_post=True)

    # access matplotlib axes
    ax = pp.plotters[0].ax

    # add borders with cartopy
    resol = '10m'
    lakes = cf.NaturalEarthFeature(category='physical', name='lakes', scale=resol, edgecolor='k', facecolor='k')
    ax.add_feature(cf.BORDERS)
    ax.add_feature(lakes)

    # go to matplotlib level
    fig = plt.gcf()
    # call this before adjusting cbar, as it will be overwritten what you specify for the cbar
    fig.tight_layout()

    # reposition colorbar
    pos1 = fig.axes[1].get_position()
    yshift = pos1.height * 1.5
    pos2 = [pos1.x0, pos1.y0 + yshift, pos1.width, pos1.height]
    fig.axes[1].set_position(pos2)
    
    if (config.has_section('coord')):
        name_coord = config.get('coord','name')
        name_coord = name_coord.split(', ')
        lon_coord = config.get('coord','lon')
        lon_coord = lon_coord.split(', ')
        lon_coord = list(map(float,lon_coord))
        lat_coord = config.get('coord','lat')
        lat_coord = lat_coord.split(', ')
        lat_coord = list(map(float,lat_coord))
        llon = lonmax-lonmin
        llat = latmax-latmin
        for i in range(0,len(name_coord)):
            pos_lon = (lon_coord[i]-lonmin)/llon
            pos_lat = (lat_coord[i]-latmin)/llat
            fig.axes[0].plot(pos_lon, pos_lat, 'r', marker='*', markersize=10, transform=fig.axes[0].transAxes)
            fig.axes[0].text(pos_lon+llon*0.003, pos_lat+llat*0.003, name_coord[i], transform=fig.axes[0].transAxes)

    # save figure
    output_dir = Path(args.output_dir)
    output_file = Path(output_dir,args.output_file)
    output_dir.mkdir(parents=True,exist_ok=True)
    print("The output is saved as " + str(output_file))
    plt.savefig(output_file)
    #psy.close('all')
