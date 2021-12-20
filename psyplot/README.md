# Description
mapplot.py plots the values of a variable from an ICON output file on a lat-lon map using a colorbar

# Set config options and flags
Different options can be set in the config file (check the example config_mapplot.ini)
Run mapplot.py with the flags -c (path to config file), -i (path to ICON output file),
and optionally -d (directory to save output) and -o (name of output file).

# Run mapplot.py on conda environment
Export path to conda (if not set)

    export PATH=".../miniconda3/bin:$PATH"

Create a conda environement with python[version>=3.7,<3.10] (psy-view requirement): 
    
    conda create -n psyplot python=3.9.7

Activate environment: 
    
    conda activate psyplot

Install requirements: 
    
    conda install -c conda-forge --file requirements.txt

Run mapplot.py: 
    
    python mapplot.py -c config_mapplot.ini -i path_to_my_nc_file -d dir_output_file -o name_output_file

# General remark
More information on psyplot can be found here: https://psyplot.github.io.
Whenever using psyplot for a publication it should be cited https://psyplot.github.io/psyplot/#how-to-cite-psyplot.
Feel free to adapt/add options in the README file, mapplot.py and config_mapplot.ini.

