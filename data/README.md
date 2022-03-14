# data 
**Description:**

Example datasets for testing the plotting routines are provided on the IAC FTP server. To download the data, run the installation insctruction for psyplot in the main directory before calling get_data:

    python get_data.py

This script calls two functions, get_data and get_example_data. 

### get_data 
```get_data()``` will download five datasets: 'my_exp1_atm_3d_ml_20180921T000000Z.nc' (output file containing grid information), 'lfff01000000.nc' (output file not containing grid information), 'ICON-1E_DOM01.nc' (file containing the grid information for 'lfff01000000.nc') and the files 'icon_19790101T000000Z.nc' and 'icon_19790101T000000Zc.nc' provided by Philipp Sommer for the transect example.

### get_example_data 
```get_example_data()``` downloads all files within 3 other directories, grib, nc and grids. They are downloaded to within folders with these same names, in a directory 'example_data'. The data within these folders is listed below (more details to come shortly):

**grib** (GRIB data)
* i1effsurf000_001
* lfff00000000
* lfff00000000_vn
* lfff00000000z_vn
* lfff00010000
* mch_bench_r19b07_dev_atm_3d_ml_20210620T120000Z.grb
* vnvt00010000

**nc** (NETCDF data)
* icon_grid_demo.nc
* laf2021112300
* lfff00000000z

**grids** (Grid files .nc)
* domain1_DOM01_r19b07.nc
* domain1_DOM01_r19b08.nc
* icon_grid_0001_R19B08_L.nc
* icon_grid_0001_R19B08_mch.nc


