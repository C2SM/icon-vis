# difference map
**Description:**

The difference_map routine plots the absolute or relative difference between the values of a variable from two ICON output file on a lat-lon map using a colorbar. The difference_map.py script works together with a config file and is described below. Alternatively, a jupyter notebook (difference_map.ipynb) with the same functionalities is provided. Follow the installation instruction in the main folder or activate your virtual environment before running the script or starting the jupyter notebook.

**Set config options and flags:**

Different options can be set in the config file (config_difference_map.ini). You can see all available options with the -co flag:

    python difference_map.py -co

**Run difference_map.py:**

Run difference_map.py with the flags -c (path to config file), -i1 (path to first ICON output file), -i2 (path to second ICON output file),
and optionally -d (directory to save output) and -o (name of output file).

    python difference_map.py -c config_difference_map.ini -i2 path_to_my_nc_file1 -i2 path_to_my_nc_file2 -d dir_output_file -o name_output_file

### Example plot 

To create the example plot below, once you have already downloaded the example data, `cd difference_map` and run:

    python difference_map.py \
    -c config_difference_map.ini \
    -i1 ../data/example_data/nc/my_exp1_atm_3d_ml_20180921T000000Z.nc \
    -i2 ../data/example_data/nc/my_exp1_diff.nc \
    -d . \
    -o test_difference_map
    
<p align="center">
<img src=difference_map/difference_map_example.png width="550"/>
</p>
