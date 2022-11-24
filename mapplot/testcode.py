# Load modules
import matplotlib.pyplot as plt
import cmcrameri.cm as cmc
import cartopy.feature as cf                                                                                                        
from pathlib import Path
import psyplot.project as psy
import sys
from timefunctions import *
import datetime as dt
import pandas as pd

from iconarray.plot import formatoptions # import plotting formatoptions (for use with psyplot)
import iconarray as iconvis # import self-written modules from iconarray

simdate = dt.datetime(2019,9,12,12,00)
startdate = dt.datetime(2019,9,13,00,00)
enddate = dt.datetime(2019,9,14,00,00)
plotfreq = '1h30min'
plotdates = pd.date_range(startdate,enddate,freq=plotfreq)
print(plotdates)
for pdate in plotdates:
    print(pdate)
    print('today' + pdate.strftime('%Y/%m/%d %H:%M'))
    lt = get_lt(pdate,simdate)

    print(lt)
    filename = lfff_name(lt)
    nc_file = '/store/s83/swester/teamx/tdf_2019091212/output/19091212/'+filename
    # If necessary, add the corresponding grid file:
    grid_file = '../data/example_data/grids/ICON-1E_DOM01.nc'

    if iconvis.check_grid_information(nc_file):
        print('The grid information is available')
        data = psy.open_dataset(nc_file)
    else:
        print('The grid information is not available')
        data = iconvis.combine_grid_information(nc_file,grid_file)

    print(filename)