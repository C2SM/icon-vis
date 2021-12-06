# Interactive plotting of ICON using Geoviews

## Installation
Create and activate the environment as follows

    conda env create -f environment.yml
    conda activate icongeoviews

If you have another environment where jupyter-notebook is installed already, add the created environment to the list of kernels.

    ipython kernel install --user --name=icongeoviews

Alternatively, if you do not have an installation of jupyter-notebook yet, install it into the current environment

    conda install -c conda-forge jupyterlab