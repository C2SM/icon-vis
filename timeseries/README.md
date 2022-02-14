# timeseries
**Description:**

The routine timeseries.py plots the values of a variable over time. The current example takes the mean over the whole map and adds the standard deviation (more options to come).

**Set config options and flags:**

Different options can be set in the config file (config_timeseries.ini). You can see all available options with the -co flag:

    python timeseries.py -co

**Run timeseries.py:**

Run timeseries.py with the flags -c (path to config file), -i (path to ICON output file),
and optionally -d (directory to save output) and -o (name of output file).

    python timeseries.py -c config_timeseries.ini -i path_to_my_nc_file -d dir_output_file -o name_output_file
