# vertical_profile 

**Description:**

The vertical_profile routine plots the values of a variable over height. The current example either takes the mean over the whole map or from a specified grid cell point. The vertical_profile.py script works together with a config file and is described below. Alternatively, a jupyter notebook (vertical_profile.ipynb) with the same functionalities is provided. Follow the installation instruction in the main folder or activate your virtual environment before running the script or starting the jupyter notebook.

**Set config options and flags:**

Different options can be set in the config file (config_vertical_profile.ini), e.g., the variable you want to plot, the name of the vertical dimension in your data, and the grid file for example if plotting GRIB data. You can see all available options with the -co flag:

    python vertical_profile.py -co

**Run vertical_profile.py:**

Run vertical_profile.py with the flags -c (path to config file), -i (path to ICON output file),
and optionally -d (directory to save output) and -o (name of output file).

    python vertical_profile.py -c config_vertical_profile.ini -i path_to_my_nc_file -d dir_output_file -o name_output_file
    
    
### Example plot 

To create the example plot below, once you have already downloaded the example data, `cd vertical_profile` and run:

    python vertical_profile.py \
    -c config_vertical_profile.ini \
    -i ../data/example_data/nc/my_exp1_atm_3d_ml_20180921T000000Z.nc \
    -d . \
    -o test_output_vertical_profile
    
<p align="center">
<img src=vertical_profile_example.png width="500"/>
</p>
