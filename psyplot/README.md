# Description
[psyplot](https://psyplot.github.io) is a Python library developped for plotting on unstructured grids like ICON.
For visualizing data along a transect, [psy-transect](https://github.com/psyplot/psy-transect) is currently under development.

# Get started with psyplot
Export path to conda (if using daint or euler: install miniconda on scratch to avoid memory issues)

    export PATH="~/miniconda3/bin:$PATH"

Create a conda environement with python[version>=3.7,<3.10] (psy-view requirement): 
    
    conda create -n psyplot python=3.9.7

Activate environment (use "source activate" in case "conda activate" does not work): 
    
    conda activate psyplot

Install requirements: 
    
    conda install -c conda-forge --file ~/icon-vis/psyplot/requirements.txt

You can install psy-transect with (not officially released yet):

    python -m pip install --user -U git+https://github.com/psyplot/psy-transect

# Use plotting routine mapplot.py
**Description:**

The routine mapplot.py plots the values of a variable from an ICON output file on a lat-lon map using a colorbar:
![mapplot example](https://github.com/C2SM/icon-vis/tree/master/psyplot/mapplot_example.png)

**Set config options and flags:**

Different options can be set in the config file (config_mapplot.ini). You can see all available options with the -co flag:

    python mapplot.py -co

**Run mapplot.py:** 

Run mapplot.py with the flags -c (path to config file), -i (path to ICON output file),
and optionally -d (directory to save output) and -o (name of output file).

    python mapplot.py -c config_mapplot.ini -i path_to_my_nc_file -d dir_output_file -o name_output_file

# General remark
Whenever using psyplot for a publication it should be cited https://psyplot.github.io/psyplot/#how-to-cite-psyplot.
Feel free to adapt/add options in the README file, mapplot.py and config_mapplot.ini.

