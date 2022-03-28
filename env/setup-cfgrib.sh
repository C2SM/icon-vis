#!/bin/bash

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
    echo 'Setting GRIB_DEFINITION_PATH for cf-grib engine'

    module load cray-python
    source /project/g110/spack/user/daint/spack/share/spack/setup-env.sh

    cosmo_eccodes=`spack location -i cosmo-eccodes-definitions@2.19.0.7%gcc@8.3.0`
    eccodes=`spack location -i eccodes@2.19.0%gcc@8.3.0+build_shared_libs`

    export GRIB_DEFINITION_PATH=${cosmo_eccodes}/cosmoDefinitions/definitions/:${eccodes}/share/eccodes/definitions/
    export OMPI_MCA_pml="ucx" 
    export OMPI_MCA_osc="ucx"
fi