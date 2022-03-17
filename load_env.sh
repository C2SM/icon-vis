#!/bin/bash

# This script is for tsa. TODO: Adapt for daint.

# ---- required for cf-grib engine ------

if [[ $HOST == *'tsa'* ]]; then
    echo 'Loading modules for cf-grib engine'
    source ~osm/.opr_setup_dir
    export PATH=$OPR_SETUP_DIR/bin:$PATH
    export MODULEPATH=$MODULEPATH\:$OPR_SETUP_DIR/modules/modulefiles
    
    module load PrgEnv-gnu/19.2
    module load eccodes/2.19.0-gnu-8.3.0-nocuda-noomp
    module load eccodes_cosmo_resources/2.19.0.5
elif [[ $HOST == *'daint'* ]]; then
    echo 'Loading modules for cf-grib engine'
    module load ecCodes/2.23.0-CrayGNU-21.09
fi

echo 'Activating virtual env'
if [[ $HOST == *'tsa'* ]]; then
    source /project/g110/pyvis/venv_tsa/bin/activate
elif [[ $HOST == *'daint'* ]]; then
    export EASYBUILD_PREFIX=/project/g110/pyvis
    module load daint-gpu EasyBuild-custom PROJ GEOS cray-python
    source /project/g110/pyvis/venv_daint/bin/activate
fi

