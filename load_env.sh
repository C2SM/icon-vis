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

    export GRIB_DEFINITION_PATH=/project/g110/spack-install/tsa/cosmo-eccodes-definitions/2.19.0.7/gcc/zcuyy4uduizdpxfzqmxg6bc74p2skdfp/cosmoDefinitions/definitions/:/project/g110/spack-install/tsa/eccodes/2.19.0/gcc/viigacbsqxbbcid22hjvijrrcihebyeh/share/eccodes/definitions/
    export GRIB_SAMPLES_PATH=/project/g110/spack-install/tsa/cosmo-eccodes-definitions/2.19.0.7/gcc/zcuyy4uduizdpxfzqmxg6bc74p2skdfp/cosmoDefinitions/samples/:/project/g110/spack-install/tsa/eccodes/2.19.0/gcc/viigacbsqxbbcid22hjvijrrcihebyeh/share/eccodes/samples/
    
elif [[ $HOST == *'daint'* ]]; then
    echo 'Setting GRIB_DEFINITION_PATH for cf-grib engine'

    module load cray-python
    source /project/g110/spack/user/daint/spack/share/spack/setup-env.sh

    cosmo_eccodes=`spack location -i cosmo-eccodes-definitions@2.19.0.7%gcc@8.3.0`
    eccodes=`spack location -i eccodes@2.19.0%gcc@8.3.0+build_shared_libs`

    export GRIB_DEFINITION_PATH=${cosmo_eccodes}/cosmoDefinitions/definitions/:${eccodes}/share/eccodes/definitions/
    export OMPI_MCA_pml="ucx" 
    export OMPI_MCA_osc="ucx"
    export ECCODES_DIR=${eccodes}

fi

if [[ $HOST == *'tsa'* ]]; then
    echo 'Setting FIELDEXTRA_PATH for tsa'
    export FIELDEXTRA_PATH=/project/s83c/fieldextra/tsa/bin/fieldextra_gnu_opt_omp
elif [[ $HOST == *'daint'* ]]; then
    echo 'Setting FIELDEXTRA_PATH for daint'
    export FIELDEXTRA_PATH=/project/s83c/fieldextra/daint/bin/fieldextra_gnu_opt_omp
fi

echo 'Activating virtual env'
if [[ $HOST == *'tsa'* ]]; then
	module use /apps/common/UES/sandbox/kraushm/tsa-PROJ/modules/all
	module load PrgEnv-gnu proj/8.0.0-fosscuda-2019b geos
    module load eccodes
    source /project/g110/pyvis/venv_tsa/bin/activate
elif [[ $HOST == *'daint'* ]]; then
    export EASYBUILD_PREFIX=/project/g110/pyvis
    module load daint-gpu EasyBuild-custom PROJ GEOS cray-python
    source /project/g110/pyvis/venv_daint/bin/activate
fi

