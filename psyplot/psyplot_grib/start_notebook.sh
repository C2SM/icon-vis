#!/bin/bash

# This script is for tsa. TODO: Adapt for daint.

# ---- required for cf-grib engine ------
echo 'Loading modules for cf-grib engine'
source ~osm/.opr_setup_dir
export PATH=$OPR_SETUP_DIR/bin:$PATH
export MODULEPATH=$MODULEPATH\:$OPR_SETUP_DIR/modules/modulefiles
 
module load PrgEnv-gnu/19.2
module load eccodes/2.19.0-gnu-8.3.0-nocuda-noomp
module load eccodes_cosmo_resources/2.19.0.5

# echo 'Loading modules for icontools'
# module load python
# source /project/g110/spack/user/tsa/spack/share/spack/setup-env.sh
# spack load icontools
# export ECCODES_DEFINITION_PATH=/oprusers/osm/opr.rh7.9/modules/eccodes_cosmo_resources/2.19.0.5/definitions ! this breaks cf-grib engine

echo 'Setting up notebook'
# ---- conda init and start jupter notebook ------
source ${SCRATCH}/etc/profile.d/conda.sh # you may need to change this to your conda path
conda activate psyplot
jupyter-notebook



# spack location -i icontools