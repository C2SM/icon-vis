# 2-dimensional mapplot of surface height
# based on an example by Philipp Sommer:
#  https://63-304997261-gh.circle-artifacts.com/0/docs/html/general/example_extending_psyplot.html   
# Date: October 14, 2021
# Author: Stephanie Westerhuis

####################
# A) Python packages
####################

# load required python packages
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.feature as cf
import cartopy.crs as ccrs
import psyplot.project as psy
import configparser
from pathlib import Path
import ipdb

#####################
# B) Read config file
#####################

# read configuration
config = configparser.ConfigParser(inline_comment_prefixes='#')
config.read('config_map.ini')

# input and ouput
in_file = config.get('io','in_file')
out_dir = config.get('io','out_dir')
out_name = config.get('io','out_name')

# map appearance
lonmin = float(config.get('map','lonmin'))
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
psy.rcParams["plotter.plot2d.cmap"] = 'cividis'
mpl.rcParams['figure.figsize'] = [10., 8.]

# create psyplot instance
pp = psy.plot.mapplot(in_file,
                      name = var_name,
                      projection = projection,
                      lonlatbox = [lonmin,lonmax,latmin,latmax],
                      bounds = {'method': 'minmax', 'vmin':vmin, 'vmax':vmax},
                      )

# add grid
if add_grid:
    pp.update(datagrid=dict(color='k', linewidth=0.2))

# access matplotlib axes
ax = pp.plotters[0].ax

# add borders with cartopy
ax.add_feature(cf.BORDERS)

# title
ax.set_title(title)

# save figure
plt.savefig(Path(out_dir, out_name))

