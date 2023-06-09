# icon-vis

[![Build Status](https://jenkins-mch.cscs.ch/job/iconvis_testsuite/badge/icon?config=build)](https://jenkins-mch.cscs.ch/job/IconVis/job/iconvis_testsuite/)
[![Build Status](https://jenkins-mch.cscs.ch/job/iconvis_testsuite/badge/icon?config=test)](https://jenkins-mch.cscs.ch/job/IconVis/job/iconvis_testsuite/)

## Introduction
This repo is a collection of python scripts to visualise ICON-simulations on the unstructered grid. The different folders contain example code for various types of plots. Example datasets for testing can be downloaded following the instructions in the [data](https://github.com/C2SM/icon-vis/tree/master/data) folder. Example plots for each folder are shown below. More detailed descriptions for each plot are in the README files of the different folders. The routines are mainly based on the python library  [psyplot](https://psyplot.github.io). The [C2SM/iconarray](https://github.com/C2SM/iconarray) python package was developed together with icon-vis, to contain the modules used in this repository.
For visualizing data along a transect, [psy-transect](https://github.com/psyplot/psy-transect) is currently under development.

If you have any feature requests, feel free to raise an issue or contact us by email. We are also happy if you want so share your own plotting scripts.

# Table of contents
1. [Introduction](#introduction)
2. [Environment Setup](#environment-setup)
    - [Install Miniconda](#install-miniconda)
    - [Create conda environment](#create-conda-environment)
    - [Run scripts on jupyter kernel](#run-scripts-on-jupyter-kernel)
3. [Example Plots](#example-plots)
    - [Map Plot](#map-plot)
    - [Vector Plot](#vector-plot)
    - [Difference Map](#difference-map)
    - [Categorical Map](#categorical-map)
    - [Timeseries](#timeseries)
    - [Vertical Profile](#vertical-profile)
    - [Transect](#transect)
    - [Combined Map Plot](#combined-map-plot)
    - [Edge Map Plot](#edge-map-plot)
4. [Usage](#usage)
    - [Notebooks and Scripts](#notebooks-and-scripts)
    - [Example Data](#example-data)
    - [Modules](#modules)
    - [Formatoptions](#formatoptions)
    - [Plotting Derived Variables](#plotting-derived-variables)
    - [Plotting with GRIB/NETCDF](#plotting-gribnetcdf-icon-data)
    - [Specifying Vertical Level](#specifying-vertical-level)
5. [FAQ](#faq)
    - [Trouble shooting](#trouble-shooting)
6. [Contacts](#contacts)
7. [Acknowledgments](#acknowledgments)


# Getting started with psyplot
## Environment Setup

We recommend to use a conda environment for the usage of the provided scripts. Please follow the instruction for the installation.

### Install Miniconda
<details>
	<summary> <b><u> Instructions </u></b> </summary>

1. Look up most recent Miniconda version for Linux 64-bit on the [Miniconda documentation pages](https://docs.conda.io/en/latest/miniconda.html)
2. Install an user specific miniconda. When the command prompt asks for the installation location, provide the path to your scratch and append the name of your miniconda version ```$SCRATCH/miniconda3``` (the default location would be on your home directory, which may lead to memory issues) and don't run ```conda init```.
        
       wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

       bash Miniconda3-latest-Linux-x86_64.sh

3. Export path to your conda installation (if using daint/euler/tsa: install miniconda on scratch to avoid memory issues).

       export PATH="$SCRATCH/miniconda3/bin:$PATH"

</details>

### Create conda environment
Create a conda environment _psyplot_ with python[version>=3.7,<3.10] (psy-view requirement) and install requirements:

    conda env create -n psyplot -f env/environment.yml

Activate environment (use "source activate" in case "conda activate" does not work):

    conda activate psyplot

If you already have the environment but want to update it:

    conda env update --file env/environment.yml --prune

If you are using the conda setup and want to use GRIB data, you will need to set the ```GRIB_DEFINITION_PATH```. This can be done on Tsa/Daint by sourcing the script ```setup-conda-env.sh```. It only needs to be run a single time, as it will save the ```GRIB_DEFINITION_PATH``` environment variable to the conda environment. You will need to deactivate and reactivate the conda environment after doing this. You can check it has been correctly set by ```conda env config vars list```. This script also sets the Fieldextra path, which is used for data interpolation. See [FAQs](#trouble-shooting) if you get an error running this.

    source env/setup-conda-env.sh

After creating the virtual environment and installing the requirements, the environment only needs to be activated for future usage. Make sure that the path is exported to ```~/miniconda3/bin```.

### Run scripts on jupyter kernel
If you have jupyter notebook installed, you can run the ipython scripts (.ipynb) by opening ```jupyter notebook``` after sourcing your _psyplot_ environment. For Piz Daint please follow the instructions below.

<details>
	<summary> <b><u> Instructions for Piz Daint </u></b> </summary>

For running the ipython scripts on Piz Daint, you need to follow the instructions on [JupyterLab on CSCS](https://user.cscs.ch/tools/interactive/jupyterlab/), which are summarized here for icon-vis:

Load the modules daint-gpu and jupyter-utils (before activating the conda environment!)

    module load daint-gpu jupyter-utils
    
Then, activate your _psyplot_ environment

    conda activate psyplot
    
Create psyplot-kernel:

    kernel-create -n psyplot-kernel

It may be necessary to export the CONDA_PREFIX, the GRIB_DEFINITION_PATH and the FIELDEXTRA_PATH in the launcher file. Therefore, open your psyplot-kernel launcher file:
	
	vim $HOME/.local/share/jupyter/kernels/psyplot-kernel/launcher
	
and add the following lines after the first line (make sure the CONDA_PREFIX points to where YOUR conda environment is located): 
	

	export CONDA_PREFIX=$SCRATCH/miniconda3/envs/psyplot
	export GRIB_DEFINITION_PATH=$SCRATCH/miniconda3/envs/psyplot/share/eccodes-cosmo-resources/definitions/:$SCRATCH/miniconda3/envs/psyplot/share/eccodes/definitions/
	export FIELDEXTRA_PATH=/project/s83c/fieldextra/daint/bin/fieldextra_gnu_opt_omp

You can now start JupyterLab with https://jupyter.cscs.ch and open the _psyplot-kernel_ notebook.

In case you need to reinstall the kernel, you can delete it with

    rm -rf $HOME/.local/share/jupyter/kernels/psyplot-kernel/

</details>


# Example plots
#### Map Plot:
See the [mapplot folder](./mapplot) for details on how this plot was made.

<p float="left">
<img src=mapplot/mapplot_example.png width="500"/>
</p>

#### Vector Plot:
See the [vectorplot folder](./vectorplot) for details on how these plots were made.

<p float="left">
<img src=vectorplot/VectorPlot_Reg.png width="450"/>
<img src=vectorplot/VectorPlot_Stream.png width="450"/>
</p>


#### Difference Map:
See the [difference_map folder](./difference_map) for details on how this plot was made.
<p float="left">
<img src=difference_map/difference_map_example.png width="550"/>
</p>

#### Categorical Map:
See the [categorical_map folder](./categorical_map) for details on how this plot was made.
<p float="left">
<img src=categorical_map/categorical_map_plot.png width="550"/>
</p>

#### Timeseries:
See the [timeseries folder](./timeseries) for details on how this plot was made.
<p float="left">
<img src=timeseries/timeseries_example.png width="500"/>
</p>

#### Vertical Profile:
See the [vertical_profile folder](./vertical_profile) for details on how this plot was made.

<p float="left">
<img src=vertical_profile/vertical_profile_example.png width="500"/>
</p>

#### Transect:
See the [transect folder](./transect) for details on how these plots were made.
<p float="left">
<img src=transect/Figure_1_transect.png width="450"/>
<img src=transect/Figure_2_transect.png width="450"/>
</p>

#### Combined Map Plot
See the [combinedplot folder](./combinedplot) for details on how this plot was made.
<p float="left">
<img src=combinedplot/combined_plot.png width="500"/>
</p>

#### Edge Map Plot
The edgeplot folder provides examples of plotting variables defined on the edge of ICON grid cells, as opposed to the cell center.
See the [edgeplot folder](./edgeplot) for details on how the below plots were made.
<p float="left">
<img src=edgeplot/edge_scalar_plots.png width="900"/>
<img src=edgeplot/vector_edge_plot.png width="500"/>
</p>

# Usage

### Notebooks and Scripts

Within this repository there are both Jupyter Notebooks and Python scripts for various examples of plots. The Python scripts can be used with your input data as parameters, or as guidance for creating your own script which is tailored to your data or visualization needs. The scripts and notebooks often use Python modules from [iconarray](https://github.com/C2SM/iconarray/tree/main/iconarray), as well as custom [formatoptions](https://github.com/C2SM/iconarray/tree/main/iconarray/plot/formatoptions) which can be used very easily while plotting with psyplot.

### Example Data

The notebooks and example plots in this repository use data which is stored on an FTP server. This data can be downloaded by running the [get_data.py](data/get_data.py) script. `cd icon_vis/icon_vis/modules` and then run:

	python get_data.py

Or you can use the function `get_example_data` in your notebooks. More information on the data downloaded can be found in the [data folder](/data) README.

### Modules

There are a number of modules from the [C2SM/iconarray](https://github.com/C2SM/iconarray) package installed by conda (see [env/environment.yml](env/environment.yml)), which you can import like a normal python package into your scripts. To work with the modules and formatoptions from within icon-vis or elsewhere, you can add this code block to the start of your script / notebook. You will see many examples of the modules being used within the scripts in this repo.

```python
import iconarray as iconvis # import iconarray modules
from iconarray.plot import formatoptions # import plotting formatoptions (for use with psyplot)
```

Then you can use the functions or modules as needed, e.g.:

```python
iconvis.get_example_data()
```

Some of the most useful modules for plotting from [iconarray](https://github.com/C2SM/iconarray) are described here:

#### grid - [grid.py](https://github.com/C2SM/iconarray/blob/main/iconarray/backend/grid.py)

**`combine_grid_information()`** This adds the required grid information from a provided grid file to your dataset if not present. It also adds coordinates encoding to each variable, which is needed to plot using psyplot.

**`check_grid_information()`** Checks whether or not the grid data needs to be added, e.g.:

```python
if check_grid_information(nc_file):
    print('The grid information is available')
    data = psy.open_dataset(nc_file)
else:
    print('The grid information is not available')
    data = combine_grid_information(nc_file,grid_file)
```

#### utils - [utilities.py](https://github.com/C2SM/iconarray/blob/main/iconarray/core/utilities.py)

**`ind_from_latlon()`** Returns the nearest neighbouring index/es of lat-lon within given lats-lons.

**`add_coordinates()`** Returns the position of given coordinates on the plot (useful to add markers at a fixed location).

**`get_stats()`** Returns the mean of two given variables, the difference of the mean and the p values.

**`wilks()`** Returns a value for which differences are significant when data point dependencies are accounted for (based on [Wilks 2016](https://journals.ametsoc.org/view/journals/bams/97/12/bams-d-15-00267.1.xml)).

**`show_data_vars()`** Returns a table with variables in your data. The first column shows the variable name psyplot will need to plot that variable.
This is useful if you plot GRIB data, because if `GRIB_cfVarName` is defined, cfgrib will set this as the variable name, as opposed to `GRIB_shortName` which you might expect.

#### interpolate.py - [interpolate.py](https://github.com/C2SM/iconarray/blob/main/iconarray/core/interpolate.py)

The functions in interpolate.py are used to facilitate the interpolation of ICON vector data to a regular grid, or a coarser ICON grid, for the purpose of vectorplots, e.g., wind plots. For psyplot we recommend to plot wind data on the regular grid as you can then scale the density of arrows in a vector plot as desired.

**`remap_ICON_to_ICON()`** This calls the `create_ICON_to_ICON_remap_namelist()` function to create a fieldextra namelist with your datafile, and subsequently runs fieldextra with this namelist. The output file along with a LOG and the namelist are saved in a `tmp` folder. The function returns the file location of the output file.

**`remap_ICON_to_regulargrid()`** This calls the `create_ICON_to_Regulargrid_remap_nl()` function to create a fieldextra namelist with your datafile, and subsequently runs fieldextra with this namelist. The output file along with a LOG and the namelist are saved in a `tmp` folder. The function returns the file location of the output file.

<hr>

Descriptions of the formatoption modules and data modules can be found in [Example Data](#example-data) and [Formatoptions](#formatoptions) sections.

### Formatoptions

Psyplot has a large number of ‘formatoptions’ which can be used to customize the look of visualizations. For example, the descriptions of the formatoptions associated with the MapPlotter class of psyplot can be found in the [psyplot documentation](https://psyplot.github.io/psy-maps/api/psy_maps.plotters.html#psy_maps.plotters.MapPlotter). The documentation for using formatoptions is also all on the psyplot documentation, or seen in the [examples](https://psyplot.github.io/examples/index.html).

Psyplot is designed in a way that is very modular and extensible, allowing users to easily create custom formatoptions and register them to plotters. Instructions for doing so are [here](https://psyplot.github.io/examples/general/example_extending_psyplot.html#3.-The-formatoption-approach).

The iconarray repository includes various [custom formatoptions](https://github.com/C2SM/iconarray/tree/main/iconarray/plot/formatoptions), that are not included in psyplot. For example:

* Borders - Adds internal land borders to mapplot, vectorplots, and combinedplots.
* Rivers - Adds rivers to mapplot, vectorplots, and combinedplots.
* Lakes - Adds lakes to mapplot, vectorplots, and combinedplots.
* Standard Title - Adds a descriptive title based on your data to your mapplot.
* Mean Max Wind - Work In Progress.
* Custom Text - Work In Progress.

We encourage you to create your own formatoptions and contribute to this repository if they would be useful for others.

Once registered to a plotter class, the formatoptions can be used as seen in many of the scripts, for example in [mapplot.py](/mapplot/mapplot.py).

### Plotting Derived Variables

If you want to plot derived variables, psyplot requires that the new variable has the correct coordinate encoding. These need to be set by you. For example, if you create a variable `delta_t` on your dataset `ds`, based on temperature calculated on the cell center, then you must set:
```python
ds.delta_t.encoding['coordinates'] = 'clat clon'
```
Whereas if your derived variable is an edge variable, for example derived from the tangential and normal components of the wind on the edges (`VN`, `VT`), then the coordinates encoding should be set as:
```python
ds.derived_edge_var.encoding['coordinates'] = 'elat elon'
```
You should also ensure that you have the cell or edge data required from the grid merged in the dataset. For variables on the cell center, your dataset will need not only `clat`, `clon`, but the bounds `clon_bnds`, `clat_bnds`, and the relationship must be defined between them, e.g.:

```python
ds.clon.attrs['bounds'] = 'clon_bnds'
ds.clat.attrs['bounds'] = 'clat_bnds'
```

Likewise for edge variables, your dataset will require `elat`, `elon`, as well as:

```python
ds.elon.attrs['bounds'] = 'elon_bnds'
ds.elat.attrs['bounds'] = 'elat_bnds'
```

The function `combine_grid_information` in the [grid.py](https://github.com/C2SM/iconarray/blob/main/iconarray/backend/grid.py) module of iconarray sets the bounds attributes (among others) while merging the required grid data with the dataset.

### Plotting GRIB/NETCDF ICON Data

#### NETCDF

NETCDF data often has everything you need to plot the data using psyplot, but sometimes it doesn't. For example the data could be missing the grid data, which is required for plotting. In this case the grid information can be added using the `combine_grid_information` function in the [grid.py](https://github.com/C2SM/iconarray/blob/main/iconarray/backend/grid.py) module. You just need to provide the location to the corresponding grid file. If you still have trouble plotting, check that the encoding coordinates for the variable you want to plot are set correctly - see [Plotting Derived Variables](#plotting-derived-variables) for more information.

#### GRIB

To open GRIB data using psyplot or xarray, you will need to use the `cfgrib` engine. eg:

```python
ds =  psy.open_dataset(icon_grib_file, engine='cfgrib', backend_kwargs={'indexpath': '', 'errors': 'ignore'})
```

GRIB data does not contain the grid information. This needs to be merged, and can be done using the `combine_grid_information` function in the [grid.py](https://github.com/C2SM/iconarray/blob/main/iconarray/backend/grid.py) module. You can provide either the file locations or xarray datasets to this function. This also sets the encoding coordinates as required.

The `cfgrib` engine relies on an eccodes installation. The easiest way to set up your environment with the required dependencies for cfgrib is to use the [Conda](#create-conda-environment) setup.

### Specifying Vertical Level

You can specify the vertical level (height/altitude/pressure levels) at which you are plotting data by specifying the `z` formatoption. This specifies the index of the vertical level array.

:bangbang: **Be careful** which direction your vertical level data is sorted, since the order direction could be changed by post processing tools.

```python
myplot = ds.psy.plot.mapvector(time=0, name=[['U', 'V']], z=8)
```

You can see which vertical dimension and value this corresponds to by printing the axes of the plot.

```python
print(myplot.axes)

# OrderedDict([(<GeoAxesSubplot:title={'center':'Vector Plot after interpolating ICON data to Regular Grid'}>,
#	      psyplot.project.Project([    arr11: 3-dim DataArray of U, V, with (variable, y_1, x_1)=(2, 101, 101),
#             time=2021-11-23, grid_mapping_1=b'', z_1=1.05e+04]))])
```

Alternatively you can specify the vertical level using the dimension name. E.g., if the name of the vertical dimension is generalVerticalLayer:

```python
myplot = ds.psy.plot.mapvector(time=0, name=[['U', 'V']], generalVerticalLayer=8)
```

# FAQ

If you have specific question about plotting, you can write that into the discussion section or check if you find the answer there already: [icon-vis disucssion](https://github.com/C2SM/icon-vis/discussions/categories/q-a)


## Trouble shooting

1. Problems setting conda environment variables via `source env/setup-conda-env.sh`. 

	> __init__() got an unexpected keyword argument 'capture_output'

	Check for outdated spack commands in your $HOME/.bashrc (should align with instruction in [C2SM spack Documentation](https://c2sm.github.io/spack-c2sm/Install.html#automatically-source-preinstalled-spack-instance), and if using VS Code/Remote-SSH you might also need to uncheck **Remote.SSH: Use Local Server** in your VS Code Remote-SSH settings, to force a new connection upon reconnecting.

2. Value error on `psy.open_dataset(f_grib2, engine="cfgrib", ...)`

	> ValueError: conflicting sizes for dimension 'values': length 1567452 on 'VN' and length 1043968 on {'generalVerticalLayer': 'generalVerticalLayer', 'values': 'P'}

	Solution: You might be trying to open a heterogeneous GRIB file with multiple hypercubes. Try `cfgrib.open_datasets` (open_datasets with an **s**!) which automates the selection of appropriate filter_by_keys and returns a list of all valid xarray.Dataset's in the GRIB file (see [cfgrib Documentation](https://github.com/ecmwf/cfgrib)).
	
```python
import cfgrib 
cfgrib.open_datasets(f_grib2, engine="cfgrib", backend_kwargs={'indexpath': '', 'squeeze':False}) 
```

3. The psyplot library needs the boundary variables (clon_bnds, clat_bnds). If they are not in the nc file, the information needs to be added with a grid file. The error is likely to be:
	> *ValueError: Can only plot 2-dimensional data!*

	Solutions: Add the path to a grid file in the config under the section 'var' with the option 'grid_file'.
	Equally you could use the function combine_grid_information in the grid module if you do not use the config file.

4. *ValueError: numpy.ndarray size changed, may indicate binary incompatibility.*

    Can be solved by reinstalling numpy:

        pip uninstall numpy

        pip install numpy

5. *ImportError: libproj.so.22: cannot open shared object file: No such file or directory*

    For some reason the LD_LIBRARY_PATH is set wrong (probably a daint issue). Can be solved by setting the path to the lib folder of your environment:

       export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/miniconda3/envs/your_env/lib

    More information on this issue: https://github.com/conda-forge/cartopy-feedstock/issues/93

6. *AttributeError: 'MapTransectMapPlot2D' object has no attribute 'convert_coordinate'*

    That's a psyplot 1.4.1 error and should be resolved by installing the newest version of psyplot.

    _Note: make sure there are no psyplot packages installed on the local user, e.g., under /users/username/.local/lib/python3.9/site-packages/. If there are, they need to be uninstalled and installed again._
    
7. *Random error in a python package pointing to /users/username/.local/lib/python3.9/site-packages/ instead of your environment*

    Deactivate your environment and uninstall the package causing the error with `pip uninstall`. Now activate your environment again and the package should now point to the right location. Update your conda environment if not.

8. *TypeError: an integer is required*

    This error points at an incompatibility between the installed library versions and the base python version. While the cause for this error is not fully understood, loading the python module corresponding to your system from `env/setup-conda-env.sh` before installing conda helped in the past. 

9. *Fatal Python error: init_fs_encoding: failed to get the Python codec of the filesystem encoding
Python runtime state: core initialized
LookupError: no codec search functions registered: can't find encoding*

The content of your miniconda repo might have been deleted (happens regularly on scratch). Follow the [instructions](#install-miniconda) to reinstall miniconda.

10. *Something like:*
```
-bash: export: `QUERY:=': not a valid identifier
-bash: export: `COSMO-ECCODES-DEFINITIONS@2.19.0.7%GCC@8.3.0/COSMODEFINITIONS/DEFINITIONS/:==>': not a valid identifier
-bash: export: `ECCODES@2.19.0%GCC@8.3.0=': not a valid identifier
-bash: export: `~AEC/SHARE/ECCODES/DEFINITIONS/=': not a valid identifier
```

This error is due to same changes on Daint on 10.9.2022. To solve this issue, you need to delete your local conda version and [install miniconda](#install-miniconda) again. Don't forget to pull the newest version of icon-vis before installing the psyplot environment again.

# Contacts

This repo has been developed by:
* Annika Lauber (C2SM) - annika.lauber@c2sm.ethz.ch
* Victoria Cherkas (MeteoSwiss) - victoria.cherkas@meteoswiss.ch

# Acknowledgments
Whenever using psyplot for a publication it should be cited https://psyplot.github.io/psyplot/#how-to-cite-psyplot.
