# height_profile 

**Description:**

The height_profile routine plots the values of a variable over height. The current example either takes the mean over the whole map or from a specified grid cell point. The height_profile.py script works together with a config file and is described below. Alternatively, a jupyter notebook (height_profile.ipynb) with the same functionalities is provided. Follow the installation instruction in the main folder or activate your virtual environment before running the script or starting the jupyter notebook.

**Set config options and flags:**

Different options can be set in the config file (config_height_profile.ini). You can see all available options with the -co flag:

    python height_profile.py -co

**Run height_profile.py:**

Run height_profile.py with the flags -c (path to config file), -i (path to ICON output file),
and optionally -d (directory to save output) and -o (name of output file).

    python height_profile.py -c config_height_profile.ini -i path_to_my_nc_file -d dir_output_file -o name_output_file
