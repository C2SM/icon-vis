# icon-vis
Collection of python scripts to visualise ICON-simulations on the unstructered grid. The different folders contain example code for different kind of plots. Example datasets for testing can be downloaded following the instructions in the 'example_datasets' folder. Example plots for each folder are shown below. More detailed descriptions for each plot are in the README files of the different folders. The routines are mainly based on the python library  [psyplot](https://psyplot.github.io).
For visualizing data along a transect, [psy-transect](https://github.com/psyplot/psy-transect) is currently under development.

# Getting started with psyplot
Export path to conda (if using daint or euler: install miniconda on scratch to avoid memory issues)

    export PATH="~/miniconda3/bin:$PATH"

Create a conda environement with python[version>=3.7,<3.10] (psy-view requirement):

    conda create -n psyplot python=3.9.7

Activate environment (use "source activate" in case "conda activate" does not work):

    conda activate psyplot

Install requirements:

    conda install -c conda-forge --file ~/icon-vis/requirements.txt

You can install psy-transect with (not officially released yet):

    python -m pip install --user -U git+https://github.com/psyplot/psy-transect

After creating the virtual environment and installing the requirements, the environment only needs to be activated for future usage. Make sure that the path is exported to ~/miniconda3/bin.

# Example plots
**mapplot:**

<img src=mapplot/mapplot_example.png width="500"/>

**timeseries:**

<img src=timeseries/timeseries_example.png width="500"/>

**height_profile:**

<img src=height_profile/height_profile_example.png width="500"/>

**transect:**
<p float="left">
<img src=transect/Figure_1_transect.png width="450"/>
<img src=transect/Figure_2_transect.png width="450"/>
</p>

# General remark
Whenever using psyplot for a publication it should be cited https://psyplot.github.io/psyplot/#how-to-cite-psyplot.
Feel free to add your own routines or adding features to already existing ones.

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

