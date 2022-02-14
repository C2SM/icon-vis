# mapplot
**Description:**

The routine mapplot.py plots the values of a variable from an ICON output file on a lat-lon map using a colorbar. There is also a jupyter notebook available with the same name.

**Set config options and flags:**

Different options can be set in the config file (config_mapplot.ini). You can see all available options with the -co flag:

    python mapplot.py -co

**Run mapplot.py:** 

Run mapplot.py with the flags -c (path to config file), -i (path to ICON output file),
and optionally -d (directory to save output) and -o (name of output file).

    python mapplot.py -c config_mapplot.ini -i path_to_my_nc_file -d dir_output_file -o name_output_file

