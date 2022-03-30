# Load required python packages
import matplotlib.pyplot as plt
import cartopy.feature as cf
from pathlib import Path
import psyplot.project as psy
import argparse
import sys
import numpy as np
import cmcrameri.cm as cmc

# Add path to the icon-vis modules
data_dir = Path(Path(__file__).resolve().parents[1], 'modules')
sys.path.insert(1, str(data_dir))
from config import read_config
from grid import check_grid_information, add_grid_information
from utils import add_coordinates

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

    # B) Read config file or show available options

    #####################

    if args.co:
        print('var, name (req): name of the variable as in the nc file\n'+\
                'var, varlim (opt): lower and upper limit of color scale\n'+\
                'var, grid_file (req if file is missing grid-information): path to grid file\n'+\
                'var, time (opt): index/es of time variable (creates a range of plots between two given indexes divided by comma)\n'+\
                'map, lonmin/lonmax/latmin/latmax (opt): values for map extension\n'+\
                'map, projection (opt): projection to draw on (e.g., robin)\n'+\
                'map, add_grid (opt): set false to remove grid with lat and lon labels\n'+\
                'map, title (opt): title of plot\n'+\
                'map, cmap (opt): name of colorbar\n'+\
                'coord, name (opt): add markers at certain locations (several inputs possible)\n'+\
                'coord, lon/lat (opt): lon and lat of the locations\n'+\
                'coord, marker (opt): marker specifications for all locations\n'+\
                'coord, marker_size (opt): marker sizes for all locations\n'+\
                'coord, col (opt): colors of all markers for all locations')
        sys.exit()

    # read config file
    var, map, coord, _ = read_config(args.config_path)

    #############

    # C) Load data

    #############

    # Check if input file exists
    input_file = Path(args.input_file)
    if not input_file.is_file():
        sys.exit(args.input_file + " is not a valid file name")

    if check_grid_information(input_file):
        ds = psy.open_dataset(input_file)
    elif 'grid_file' in var.keys():
        ds = add_grid_information(input_file, var['grid_file'])
    else:
        sys.exit('The file '+str(input_file)+\
                ' is missing the grid information. Please provide a grid file in the config.')

    #############

    # D) Plotting

    #############

    # Get map extension
    if 'lonmin' not in map.keys():
        map['lonmin'] = min(np.rad2deg(ds.clon.values[:]))
    if 'lonmax' not in map.keys():
        map['lonmax'] = max(np.rad2deg(ds.clon.values[:]))
    if 'latmin' not in map.keys():
        map['latmin'] = min(np.rad2deg(ds.clat.values[:]))
    if 'latmax' not in map.keys():
        map['latmax'] = max(np.rad2deg(ds.clat.values[:]))

    # Check if several time steps should be plotted
    if len(var['time']) == 1:
        end_t = var['time'][0] + 1
    else:
        end_t = var['time'][1] + 1

    for i in range(var['time'][0], end_t):
        if 'varlim' in var.keys():
            bounds={'method': 'minmax',
                    'vmin': var['varlim'][0],
                    'vmax': var['varlim'][1]}
        else: 
            bounds=['minmax']
        # create psyplot instance
        pp = psy.plot.mapplot(ds, name=var['name'], t=i, bounds=bounds)
        if 'projection' in map.keys():
            pp.update(projection=map['projection'])
        if 'lonmin' in map.keys():
            pp.update(map_extent=[
                map['lonmin'], map['lonmax'], map['latmin'], map['latmax']
            ])
        if 'add_grid' in map.keys():
            pp.update(xgrid=map['add_grid'], ygrid=map['add_grid'])
        if 'title' in map.keys():
            pp.update(title=map['title'])
        if 'cmap' in map.keys():
            pp.update(cmap=map['cmap'])

        # access matplotlib axes
        ax = pp.plotters[0].ax

        # add borders with cartopy
        resol = '10m'
        lakes = cf.NaturalEarthFeature(category='physical',
                                       name='lakes',
                                       scale=resol,
                                       edgecolor='k',
                                       facecolor='k')
        ax.add_feature(cf.BORDERS)
        ax.add_feature(lakes)

        # go to matplotlib level
        fig = plt.gcf()

        if coord:
            llon = map['lonmax'] - map['lonmin']
            llat = map['latmax'] - map['latmin']
            for i in range(0, len(coord['lon'])):
                pos_lon, pos_lat = add_coordinates(
                    coord['lon'][i], coord['lat'][i], map['lonmin'],
                    map['lonmax'], map['latmin'], map['latmax'])
                fig.axes[0].plot(pos_lon,
                                 pos_lat,
                                 coord['col'][i],
                                 marker=coord['marker'][i],
                                 markersize=coord['marker_size'][i],
                                 transform=fig.axes[0].transAxes)
                if 'name' in coord.keys():
                    fig.axes[0].text(pos_lon + llon * 0.003,
                                     pos_lat + llat * 0.003,
                                     coord['name'][i],
                                     transform=fig.axes[0].transAxes)

    #############

    # E) Save figure

    #############

    # save figure
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        if (len(var['time']) > 1):
            name_file = args.output_file + '_' + str(i)
        else:
            name_file = args.output_file
        output_file = Path(output_dir, name_file)
        print("The output is saved as " + str(output_file))
        plt.savefig(output_file)
