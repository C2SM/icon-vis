#!/bin/bash

if [[ $HOST == *'tsa'* ]]; then
    echo 'Setting GRIB_DEFINITION_PATH for cfgrib engine'
    module load python
    source /project/g110/spack/user/admin-tsa/spack/share/spack/setup-env.sh

    cosmo_eccodes=`spack find --format "{prefix}" cosmo-eccodes-definitions@2.19.0.7%gcc | head -n1`
    eccodes=`spack find --format "{prefix}" eccodes@2.19.0%gcc ~aec | head -n1`
    export GRIB_DEFINITION_PATH=${cosmo_eccodes}/cosmoDefinitions/definitions/:${eccodes}/share/eccodes/definitions/
    export OMPI_MCA_pml="ucx"
    export OMPI_MCA_osc="ucx"
    echo 'GRIB_DEFINITION_PATH: '${GRIB_DEFINITION_PATH}
    conda env config vars set GRIB_DEFINITION_PATH=${GRIB_DEFINITION_PATH}
elif [[ $HOST == *'daint'* ]]; then
    echo 'Setting GRIB_DEFINITION_PATH for cfgrib engine'
    module load cray-python
    source /project/g110/spack/user/admin-daint/spack/share/spack/setup-env.sh

    cosmo_eccodes=`spack find --format "{prefix}" cosmo-eccodes-definitions@2.19.0.7%gcc | head -n1`
    eccodes=`spack find --format "{prefix}" eccodes@2.19.0%gcc ~aec | head -n1`
    export GRIB_DEFINITION_PATH=${cosmo_eccodes}/cosmoDefinitions/definitions/:${eccodes}/share/eccodes/definitions/
    export OMPI_MCA_pml="ucx"
    export OMPI_MCA_osc="ucx"
    echo 'GRIB_DEFINITION_PATH: ' ${GRIB_DEFINITION_PATH}
    conda env config vars set GRIB_DEFINITION_PATH=${cosmo_eccodes}/cosmoDefinitions/definitions/:${eccodes}/share/eccodes/definitions/
fi

# ---- required for fieldextra ------

if [[ $HOST == *'tsa'* ]]; then

    echo 'Setting FIELDEXTRA_PATH for tsa'
    conda env config vars set FIELDEXTRA_PATH=/project/s83c/fieldextra/tsa/bin/fieldextra_gnu_opt_omp

elif [[ $HOST == *'daint'* ]]; then

    echo 'Setting FIELDEXTRA_PATH for daint'
    conda env config vars set FIELDEXTRA_PATH=/project/s83c/fieldextra/daint/bin/fieldextra_gnu_opt_omp

fi

# ---- required for cartopy ------

echo 'Make sure to deactivate your environment completely before reactivating (i.e., you should not be in a base environment). To make sure, you can run conda deactivate twice'
echo 'Enable cartopy to modify cartopy.config by placing siteconfig.py in cartopy package'
vpython=$(ls --color=never -d $CONDA_PREFIX/lib/python*);
cp env/siteconfig.py ${vpython}/site-packages/cartopy
