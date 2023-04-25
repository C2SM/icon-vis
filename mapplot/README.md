# Map plot
**Description:**

The mapplot routine plots the values of a variable from an ICON output file on a lat-lon map using a colorbar. The mapplot.py script works together with a config file and is described below. Alternatively, a jupyter notebook (mapplot.ipynb) with the same functionalities is provided. Follow the installation instruction in the main folder or activate your virtual environment before running the script or starting the jupyter notebook.

**Set config options and flags:**

Different options can be set in the config file (config_mapplot.ini). You can see all available options with the -co flag:

    python mapplot/mapplot.py -co
    
If you want to add any other formatoption, you will need to manually add a line in `mapplot/mapplot.py` somewhere before the last line, e.g., `pp.update(titlesize=30, clabelsize=20)`. All available formatoptions can be found here: [formatoptions mapplot](https://psyplot.github.io/psy-maps/generated/psyplot.project.plot.mapplot.html).

**Run mapplot.py:**

Run mapplot.py with the flags -c (path to config file), -i (path to ICON output file),
and optionally -d (directory to save output) and -o (name and type of output file).

    python mapplot/mapplot.py -c mapplot/config_mapplot.ini -i path_to_my_nc_file -d dir_output_file -o name_output_file.type

### Example plot

To create the example plot below, once you have already downloaded the example data, run:

    python mapplot/mapplot.py \
    -c mapplot/config_mapplot.ini \
    -i data/example_data/nc/my_exp1_atm_3d_ml_20180921T000000Z.nc \
    -d mapplot \
    -o test_output_mapplot.png

<p align="center">
<img src=mapplot_example.png width="500"/>
</p>
