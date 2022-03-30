# data 
**Description:**

Example datasets for testing the plotting routines are provided on the IAC FTP server. To download the data, run the installation instruction for psyplot in the main directory before calling get_data:

    python get_data.py

This script calls the function get_example_data. 

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
* my_exp1_atm_3d_ml_20180921T000000Z.nc
* my_exp1_diff.nc (manipulated file to create differences to my_exp1_atm_3d_ml_20180921T000000Z.nc)
* icon_19790101T000000Z.nc (example by Philipp Sommer for transect plot)
* icon_19790101T000000Zc.nc (example by Philipp Sommer for transect plot)
* lfff01000000.nc (corresponding grid information in ICON-1E_DOM01.nc)

**grids** (Grid files .nc)
* domain1_DOM01_r19b07.nc
* domain1_DOM01_r19b08.nc
* icon_grid_0001_R19B08_L.nc
* icon_grid_0001_R19B08_mch.nc
* ICON-1E_DOM01.nc


