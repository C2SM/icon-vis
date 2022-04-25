# timeseries
**Description:**

The timeseries routine plots the values of a variable over time. The current example either takes the mean over the whole map or from a specified grid cell point. The timeseries.py script works together with a config file and is described below. Alternatively, a jupyter notebook (timeseries.ipynb) with the same functionalities is provided. Follow the installation instruction in the main folder or activate your virtual environment before running the script or starting the jupyter notebook.

**Set config options and flags:**

Different options can be set in the config file (config_timeseries.ini). You can see all available options with the -co flag:

    python timeseries.py -co

**Run timeseries.py:**

Run timeseries.py with the flags -c (path to config file), -i (path to ICON output file),
and optionally -d (directory to save output) and -o (name of output file).

    python timeseries.py -c config_timeseries.ini -i path_to_my_nc_file -d dir_output_file -o name_output_file


### Example plot

To create the example plot below, once you have already downloaded the example data, `cd timeseries` and run:

    python timeseries.py \
    -c config_timeseries.ini \
    -i ../data/example_data/nc/icon_grid_demo.nc \
    -d . \
    -o test_output_timeseries

<p align="center">
<img src=timeseries_example.png width="500"/>
</p>
