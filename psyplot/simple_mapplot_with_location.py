# 2-dimensional mapplot of surface height
# Date: October 14, 2021
# Author: Stephanie Westerhuis
# Adapted: Nadja Omanovic
# use with config_map_simple_mapplot_with_location.ini


####################

# A) Python packages

####################

# load required python packages

import matplotlib.pyplot as plt
import matplotlib as mpl
import cmcrameri.cm as cmc
import cartopy.feature as cf
import cartopy.crs as ccrs
import configparser
from pathlib import Path
import psyplot.project as psy

#####################

# B) Read config file

#####################

# read configuration
config = configparser.ConfigParser(inline_comment_prefixes='#')
config.read('config_map_simple_mapplot_with_location.ini')

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
psy.rcParams["plotter.plot2d.cmap"] = cmc.nuuk  # 'cividis'
mpl.rcParams['figure.figsize'] = [6., 6.]

# create psyplot instance
pp = psy.plot.mapplot(in_file,
name = var_name,
projection = projection,
bounds = {'method': 'minmax', 'vmin':vmin, 'vmax':vmax}, 
map_extent=[5.8, 10.7, 45.5, 48.0],
title=title + ' on %Y-%m-%d %H:%M',
enable_post=True)

# add grid
#if add_grid:
#    pp.update(datagrid=dict(color='k', linewidth=0.2))

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

# get coordinate on plot
# coordinates Eriswil: 7.87, 47.07
# map extent in lower left corner: 5.8, 45.5
# the difference to desired coordinate point: 2 and 1.5
# norm to [0, 1]: 2 is 0.4 and 1.5 is 0.6 based on the difference to upper right corner
fig.axes[0].plot(0.4, 0.6, 'r', marker='*', markersize=10, transform=fig.axes[0].transAxes)
fig.axes[0].text(0.42, 0.6, 'Eriswil', transform=fig.axes[0].transAxes)

# save figure
plt.savefig(Path(out_dir, out_name))
#psy.close('all')
