# icon-vis
Collection of python scripts to visualise ICON-simulations on the unstructered grid. The different folders contain example code for different kind of plots. Example datasets for testing can be downloaded following the instructions in the 'example_datasets' folder. Example plots for each folder are shown below. More detailed descriptions for each plot are in the README files of the different folders. The routines are mainly based on the python library  [psyplot](https://psyplot.github.io).
For visualizing data along a transect, [psy-transect](https://github.com/psyplot/psy-transect) is currently under development.

# Table of contents
1. [Introduction](#icon-vis)
2. [Environment Setup](#environment-setup)
    - [Piz Daint](#piz-daint)
    - [Run scripts on jupyter kernel](#run-scripts-on-jupyter-kernel)
    - [Conda environment](#conda-environment)
3. [Example Plots](#example-plots)
    - [Map plot](#mapplot)
    - [Timeseries](#timeseries)
    - [Height Profile](#height_profile)
    - [Transect](#transect)
4. [Usage](#usage)
    - [Notebooks and Scripts](#notebooks-and-scripts)
    - [Example Data](#example-data)
    - [Modules](#modules)
    - [Formatoptions](#formatoptions)
6. [Contacts](#contacts)
7. [Acknowledgments](#acknowledgments)
8. [FAQs/Troubleshooting instructions](#trouble-shooting)


# Getting started with psyplot
## Environment Setup
### Piz Daint

To be able to run the scripts, you can source the pre-installed environment on Piz Daint by sourcing the load environment file:

    source ~/env/load_env.sh
    
### Run scripts on jupyter kernel
**Piz Daint**

For running the ipython scripts on Piz Daint, create a psyplot-kernel with:

    source ~/env/create_jupyter_kernel.sh

You can now start JupyterLab with https://jupyter.cscs.ch (Check [JupyterLab on CSCS](https://user.cscs.ch/tools/interactive/jupyterlab/) for more information) and open the _psyplot-kernel_ notebook. Everything should be ready to use.

### Conda environment

<details>
  <summary>Installing Miniconda on Tsa/Daint (CSCS)</summary>
  
  ### Installing Miniconda on Tsa/Daint (CSCS)
1. Look up most recent Miniconda version for Linux 64-bit on the [Miniconda documentation pages](https://docs.conda.io/en/latest/miniconda.html)
2. Install as user specific miniconda e.g. on /scratch (enter ```cd $SCRATCH``` at the command line to get to your personal scratch directory).
   When the command prompt asks for installation location, provide the path to your scratch and append ```/miniconda3```.
        
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

        bash Miniconda3-latest-Linux-x86_64.sh
  
3. Export path to your conda installation (if using daint/euler/tsa: install miniconda on scratch to avoid memory issues).

        export PATH="$SCRATCH/miniconda3/bin:$PATH"
    
</details>

Create a conda environement 'psyplot' with python[version>=3.7,<3.10] (psy-view requirement) and install requirements:

    conda env create -f env/environment.yml

Activate environment (use "source activate" in case "conda activate" does not work):

    conda activate psyplot

If you are using the conda setup and want to use GRIB data, you will need to set the ```GRIB_DEFINITION_PATH```. This can be done on Tsa/Daint by sourcing the script ```setup-cfgrib.sh```. It only needs to be run a single time, as it will save the ```GRIB_DEFINITION_PATH``` environment variable to the conda environment. You will need to deactivate and reactivate the conda environment after doing this. You can check it has been correctly set by ``` conda env config vars list```.

    source env/setup-cfgrib.sh

You can install psy-transect with (not officially released yet):

    python -m pip install git+https://github.com/psyplot/psy-transect

After creating the virtual environment and installing the requirements, the environment only needs to be activated for future usage. Make sure that the path is exported to ~/miniconda3/bin.

# Example plots
#### mapplot:
See the [mapplot folder](./mapplot) for details on how this plot was made.

<p float="left">
<img src=mapplot/mapplot_example.png width="500"/>
</p>

#### difference_map:
See the [difference_map folder](./difference_map) for details on how this plot was made.
<p float="left">
<img src=difference_map/difference_map_example.png width="550"/>
</p>

#### timeseries:
See the [timeseries folder](./timeseries) for details on how this plot was made.
<p float="left">
<img src=timeseries/timeseries_example.png width="500"/>
</p>

#### height_profile:
See the [height_profile folder](./height_profile) for details on how this plot was made.

<p float="left">
<img src=height_profile/height_profile_example.png width="500"/>
</p>

#### transect:
See the [transect folder](./transect) for details on how this plot was made.
<p float="left">
<img src=transect/Figure_1_transect.png width="450"/>
<img src=transect/Figure_2_transect.png width="450"/>
</p>

# Usage

### Notebooks and Scripts

Within this repository there are both Jupyter Notebooks and Python scripts for various examples of plots. The Python scripts can be used with your input data as parameters, or as guidance for creating your own script which is tailored to your data or visualization needs. The scripts and notebooks often use Python modules from the [modules](/modules) folder, as well as custom [formatoptions](/modules/formatoptions) which can then be used very easily while plotting with psyplot. 

### Example Data

The notebooks and example plots in this repository use data which is stored on an FTP server. This data can be downloaded by running the `data/get_data.py` script. `cd data` and then run:

	python get_data.py

Or you can use the function `get_example_data` in your notebooks. More information on the data downloaded can be found in the [data folder](/data) README.

### Modules

Description of modules coming soon.

### Formatoptions

Psyplot has a large number of ‘formatoptions’ which can be used to customize the look of visualizations. For example, the descriptions of the formatoptions associated with the MapPlotter class of psyplot can be found in the [psyplot documentation](https://psyplot.github.io/psy-maps/api/psy_maps.plotters.html#psy_maps.plotters.MapPlotter). The documentation for using formatoptions is also all on the psyplot documentation, or seen in the [examples](https://psyplot.github.io/examples/index.html).

Psyplot is designed in a way that is very modular and extensible, allowing users to easily create custom formatoptions and register them to plotters. Instructions for doing so are [here](https://psyplot.github.io/examples/general/example_extending_psyplot.html#3.-The-formatoption-approach). 

This repository includes various custom formatoptions, that are not included in psyplot. For example:

* [Borders](/modules/formatoptions/borders.py) - Adds internal land borders to mapplot, vectorplots, and combinedplots.
* [Rivers](/modules/formatoptions/rivers.py) - Adds rivers to mapplot, vectorplots, and combinedplots.
* [Lakes](/modules/formatoptions/lakes.py) - Adds lakes to mapplot, vectorplots, and combinedplots.
* [Standard Title](/modules/formatoptions/standardtitle.py) - Adds a descriptive title based on your data to your mapplot.
* [Mean Max Wind](/modules/formatoptions/meanmaxwind.py) - Work In Progress.
* [Custom Text](/modules/formatoptions/customtext.py) - Work In Progress.

We encourage you to create your own formatoptions and contribute to this repository if they would be useful for others.

Once registered to a plotter class, the formatoptions can be used as seen in many of the scripts, for example in [mapplot.py](/mapplot/mapplot.py)

# Trouble shooting
1. The psyplot library needs the boundary variables (clon_bnds, clat_bnds). If they are not in the nc file, the information needs to be added with a grid file. The error is likely to be: *ValueError: Can only plot 2-dimensional data!*

    Solution: Add the path to a grid file in the config under the section 'var' with the option 'grid_file'.

2. *ValueError: numpy.ndarray size changed, may indicate binary incompatibility.*

    Can be solved by reinstalling numpy:

        pip uninstall numpy

        pip install numpy
        
3. *ImportError: libproj.so.22: cannot open shared object file: No such file or directory*

    For some reason the LD_LIBRARY_PATH is set wrong (probably a daint issue). Can be solved by setting the path to the lib folder of your environment:
    
       export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/miniconda3/envs/your_env/lib
    
    More information on this issue: https://github.com/conda-forge/cartopy-feedstock/issues/93
    
4. *AttributeError: 'MapTransectMapPlot2D' object has no attribute 'convert_coordinate'*

    That's a psyplot 1.4.1 error and should be resolved by installing the newest version of psyplot.
    
    _Note: make sure there are no psyplot packages installed on the local user, e.g., under Users/username/.local/lib/python3.9/site-packages/. If there are, they need to be uninstalled and installed again._
    
# Contacts

This repo has been developed by:
* Annika Lauber (C2SM) - annika.lauber@c2sm.ethz.ch
* Victoria Cherkas (MeteoSwiss) - victoria.cherkas@meteoswiss.ch

# Acknowledgments
Whenever using psyplot for a publication it should be cited https://psyplot.github.io/psyplot/#how-to-cite-psyplot.
Feel free to add your own routines or adding features to already existing ones.
