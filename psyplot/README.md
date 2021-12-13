# Description
mapplot.py plots the values of a variable from an ICON output file on a lat-lon map using a colorbar

# Set config options
Different options can be set in the config file (check the example config_mapplot.ini)

# Run mapplot.py
Run mapplot.py with the flags -c (path to config file), -i (path to ICON output file),
and optionally -d (Directory to save outpu) and -o (name of output file).

# Recommended installation for conda environment
conda install -c conda-forge numpy "matplotlib<3.5" psy-view psy-reg xarray cartopy proj geos cmcrameri argparse

# General remark
More information on psyplot can be found here: https://psyplot.github.io.
Whenever using psyplot for a publication it should be cited https://psyplot.github.io/psyplot/#how-to-cite-psyplot.
Feel free to adapt/add options in the README file, mapplot.py and config_mapplot.ini.

