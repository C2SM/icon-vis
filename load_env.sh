#!/bin/bash

# This script is for tsa. TODO: Adapt for daint.

# ---- required for cf-grib engine ------

if [[ $HOST == *'tsa'* ]]; then
    # module load python/3.7.4
    # source /project/g110/spack/user/tsa/spack/share/spack/setup-env.sh

    # cosmo_eccodes=`spack location -i  cosmo-eccodes-definitions@2.19.0.7%gcc@8.3.0`
    # eccodes=`spack location -i eccodes@2.19.0%gcc`

    export GRIB_DEFINITION_PATH=/project/g110/spack-install/tsa/cosmo-eccodes-definitions/2.19.0.7/gcc/zcuyy4uduizdpxfzqmxg6bc74p2skdfp/cosmoDefinitions/definitions/:/project/g110/spack-install/tsa/eccodes/2.19.0/gcc/viigacbsqxbbcid22hjvijrrcihebyeh/share/eccodes/definitions/
    export OMPI_MCA_pml="ucx" 
    export OMPI_MCA_osc="ucx"
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

echo 'Activating virtual env'
if [[ $HOST == *'tsa'* ]]; then
	module use /apps/common/UES/sandbox/kraushm/tsa-PROJ/modules/all
	module load PrgEnv-gnu
	module load proj/8.0.0-fosscuda-2019b
	module load geos
    source /project/g110/pyvis/venv_tsa/bin/activate
elif [[ $HOST == *'daint'* ]]; then
    export EASYBUILD_PREFIX=/project/g110/pyvis
    module load daint-gpu EasyBuild-custom PROJ GEOS cray-python
    source /project/g110/pyvis/venv_daint/bin/activate
fi

