                                                                                                  
## MODULES ##
import matplotlib.pyplot as plt
import cmcrameri.cm as cmc
import cartopy.feature as cf                                                                                                        
from pathlib import Path
import psyplot.project as psy
import sys

from iconarray.plot import formatoptions # import plotting formatoptions (for use with psyplot)
import iconarray as iconvis # import self-written modules from iconarray

# extra
import pandas as pd
import datetime as dt
import numpy as np

# #own scripts
import locfunctions as lf
import varfunctions as vf
from timefunctions import *

from ipdb import set_trace

###############################################################################################
## CONSTANT FILE  ##
c_filename = "lfff00000000c.nc"
filepath = '/store/s83/swester/teamx/tdf_2019091212/output/19091212/'
const_file = filepath + c_filename
data_c = psy.open_dataset(const_file)

###############################################################################################
## DECIDE ##
# where to save
plotpath_base = '/scratch/tlezuo/icon-vis/hor_cross/'
# decide which areas to plot
areas_list = []
# areas_list.extend([lf.icon_domain,lf.eastern_alps,lf.inn_area])
areas_list=[lf.zoom]

# decide which variables to plot
pvar = vf.HSURF
# decide how to plot it
plottype = 'poly' # 'poly' = triangles,'contourf'= smoothed, 'contour'= lines

###############################################################################################
## PLOT SETUP ##
# loop 1 over areas
for area in areas_list:
    # check printout
    print('plotting area '+area.name)

    print('     plotting variable '+pvar.name )
    # path sepcific to area and variable
    plotpath = plotpath_base+str(area.name)+'/'+str(pvar.name)+'/'
    Path(plotpath).mkdir(parents=True, exist_ok=True)

        
    # title specific to area, variable, time
    title = 'A = '+str(area.name)+', VAR = '+pvar.title
    plotname = str(area.name)+'_'+pvar.name+'_'+plottype+'.png'

 
    ###############################################################################################
    ## PLOT ##
    #plot
    # set_trace()
    pp = psy.plot.mapplot(data_c,
        name = pvar.name,
        t = 0,
        projection = 'robin',
        plot=plottype,
        bounds = np.arange(pvar.min,pvar.max,pvar.ticks),#{'method': 'minmax', 'vmin':pvar.min, 'vmax':pvar.max},
        map_extent = [area.lonmin, area.lonmax, area.latmin, area.latmax],
        title = title,
        cmap=pvar.cmap,
        cticks=np.arange(pvar.min,pvar.max,pvar.ticks*5),
        clabel = pvar.name+' '+pvar.units,
        xgrid = False, ygrid = False,
        )
    # set_trace()
    #annotations
    fig = plt.gcf()
    fig.set_size_inches(7,7)
    handles_list=[]
    labels_list=[]
    for locmark in area.locmarks:
        pos_lon, pos_lat = iconvis.add_coordinates(locmark.lon,locmark.lat,area.lonmin,area.lonmax,area.latmin,area.latmax)
        fig.axes[0].plot(pos_lon, pos_lat,color=locmark.color,marker= '.', markersize=10, transform=fig.axes[0].transAxes,label=locmark.name,linestyle='None') 
        # handles_list.append(locmark.marker)
        # labels_list.append(locmark.name)
        if locmark.name == 'Station Flughafen':
            fig.axes[0].text(pos_lon-0.06, pos_lat+0.03,locmark.name, transform=fig.axes[0].transAxes,color=locmark.color,fontsize=16)
            fig.axes[0].plot(pos_lon, pos_lat,color=locmark.color,marker= '.', markersize=20, transform=fig.axes[0].transAxes,label=locmark.name,linestyle='None') 

    # fig.legend(loc='upper left', bbox_to_anchor=(0.4, 0.2))
    # save figure
    pp.update()
    plt.savefig(plotpath+plotname,dpi=300)
    plt.show()