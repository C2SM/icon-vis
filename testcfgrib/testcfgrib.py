import xarray as xr
import os
import iris_grib
import pygrib

LOGNAME = os.environ['LOGNAME']

# Make sure to have the test files available (copy from bcrezee)
# Files have to be available in folder with write permission, since
# xarray creates temporary .idx files.
# /scratch/bcrezee/example_cosmo_files
# /scratch/bcrezee/example_icon_files

# Use the geoviews environment (see folder geoviews in this repository), it includes all necessary packages


###############################################################
######### COSMO ###############################################
###############################################################


# Only one typeOfLevel per data variable is supported, therefore filter_by_keys is necessary. 
# See: https://github.com/ecmwf/cfgrib/issues/2#issuecomment-407861873
infile = f"/scratch/{LOGNAME}/example_cosmo_files/lfff00000000"
ds_cosmo = xr.open_dataset(infile, engine='cfgrib', filter_by_keys={'stepType': 'instant', 'typeOfLevel': 'surface'})
ds_cosmo.al.plot()
plt.savefig('ds_cosmo_al.png')

# How about using iris, is it simpler?
cubes = list(iris_grib.load_cubes(infile))
# No, this results in "TranslationError: Product definition section 4 contains unsupported type of second fixed surface [150]".

###############################################################
######### ICON  ###############################################
###############################################################

# Now let's try ICON.
infile = f"/scratch/{LOGNAME}/example_icon_files/lfff00000000"
# With xarray
ds_icon = xr.open_dataset(infile, engine='cfgrib', filter_by_keys={'stepType': 'instant', 'typeOfLevel': 'surface'})
# Opens, but can not read the grid... Message:
# ecCodes provides no latitudes/longitudes for gridType='unstructured_grid'

# With iris_grib
cubes = list(iris_grib.load_cubes(infile))
# TranslationError: Grid definition template [101] is not supported

# With pygrib
grbs = pygrib.open(infile)
for grb in grbs:
    print(grb)
lats, lons = grb.latlons()
# ValueError: unsupported grid unstructured_grid


# Summary: 
#    For COSMO files, one can use xarray with the right filter_by_keys arguments (a bit cumbersome... but works)
#    
#    For ICON files, all the packages tried (xarray, iris-grib, pygrib) have problems with the unstructured grid.
# 

