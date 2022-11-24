                                                                                                  
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

# #own scripts
import locfunctions as lf
import varfunctions as vf
from timefunctions import *

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
areas_list=[lf.domain_vis]

# decide which variables to plot
pvars_list = []
# pvars_list.extend([vf.qv_2m,vf.T_2M])
pvars_list= [vf.T_2M]

# decide which time to plot
simdate = dt.datetime(2019,9,12,12,00) # no change,. simulation start
startdate = dt.datetime(2019,9,13,00,00)
enddate = dt.datetime(2019,9,13,1,00)
plotfreq = '0h30min'
plotdates = pd.date_range(startdate,enddate,freq=plotfreq)

# decide how to plot it
plottype = 'contourf' # 'poly' = triangles,'contourf'= smoothed, 'contour'= lines

###############################################################################################
## PLOT SETUP ##
# loop 1 over areas
for area in areas_list:
    # check printout
    print('plotting area '+area.name)

# loop 2 over variables
    for pvar in pvars_list:
        print('     plotting variable '+pvar.name )
        # path sepcific to area and variable
        plotpath = plotpath_base+str(area.name)+'/'+str(pvar.name)+'/'
        Path(plotpath).mkdir(parents=True, exist_ok=True)
        
# loop 3 over time
        for pdate in plotdates:
            print('         plotting '+pvar.name + ' on ' + pdate.strftime('%Y/%m/%d at %H:%M')+' in '+area.name)
            # title specific to area, variable, time
            title = 'A = '+str(area.name)+', d = '+ pdate.strftime('%Y/%m/%d at %H:%M')+', VAR = '+pvar.title
            plotname = str(area.name)+pdate.strftime('%Y%m%d_%H%M')+'_'+pvar.name+'_'+plottype+'.png''.png'

            ###############################################################################################
            ## READ IN ##
            lt = get_lt(pdate,simdate) # get leadtime
            filename = lfff_name(lt) # get filename
            nc_file = filepath+filename
            # If necessary, add the corresponding grid file:
            grid_file = '/store/s83/swester/teamx/grid_R19B08_size_cosmo1/d01_DOM01.nc'

            if iconvis.check_grid_information(nc_file):
                # print('             The grid information is available')
                data = psy.open_dataset(nc_file)
            else:
                print('             The grid information is not available')
                data = iconvis.combine_grid_information(nc_file,grid_file)

            ###############################################################################################
            ## PLOT ##
            #plot
            if pvar.name == 'wind_10m':
                pp = psy.plot.mapvector(data, 
                    name=[['u_10m', 'v_10m']], 
                    )

                #annotations
                fig = plt.gcf()
                for locmark in area.locmarks:
                    pos_lon, pos_lat = iconvis.add_coordinates(locmark.lon,locmark.lat,area.lonmin,area.lonmax,area.latmin,area.latmax)
                    fig.axes[0].plot(pos_lon, pos_lat,color=locmark.color,marker='.', markersize=10, transform=fig.axes[0].transAxes) 
                    fig.axes[0].text(pos_lon+0.01, pos_lat+0.01,locmark.name, transform=fig.axes[0].transAxes)

                # save figure
                pp.update()
                plt.savefig(plotpath+plotname)
                plt.show()

            else: 
                pp = psy.plot.mapplot(data,
                    name = pvar.name,
                    t = 0,
                    projection = 'robin',
                    plot=plottype,
                    bounds = {'method': 'minmax', 'vmin':pvar.min, 'vmax':pvar.max},
                    map_extent = [area.lonmin, area.lonmax, area.latmin, area.latmax],
                    title = title,
                    cmap=pvar.cmap,
                    clabel = pvar.name+' '+pvar.units,
                    xgrid = False, ygrid = False
                    )

                #annotations
                fig = plt.gcf()
                for locmark in area.locmarks:
                    pos_lon, pos_lat = iconvis.add_coordinates(locmark.lon,locmark.lat,area.lonmin,area.lonmax,area.latmin,area.latmax)
                    fig.axes[0].plot(pos_lon, pos_lat,color=locmark.color,marker='.', markersize=10, transform=fig.axes[0].transAxes) 
                    fig.axes[0].text(pos_lon+0.01, pos_lat+0.01,locmark.name, transform=fig.axes[0].transAxes)

                # save figure
                pp.update()
                plt.savefig(plotpath+plotname)
                plt.show()