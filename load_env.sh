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
    echo 'TODO: cf-grib engine not loaded on daint'
fi

echo 'Activating virtual env'
if [[ $HOST == *'tsa'* ]]; then
    source /project/g110/pyvis/venv_tsa/bin/activate
elif [[ $HOST == *'daint'* ]]; then
    source /project/g110/pyvis/venv_daint/bin/activate
fi

