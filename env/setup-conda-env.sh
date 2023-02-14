#!/bin/bash

function check_python {
    python_version_l=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
    python_version_maj=$(python -c 'import sys; print(".".join(map(str, sys.version_info[0:1])))')
    python_version_min=$(python -c 'import sys; print(".".join(map(str, sys.version_info[1:2])))')
    python_lib=$(python --version | tr '[:upper:]' '[:lower:]' | sed 's/ //g' | sed 's/\.[^.]*$//')

    min_required_maj=3
    min_required_min=9
    if [[ $(echo $python_version_maj'>='$min_required_maj | bc -l) == 1  ]]  && [[ $(echo $python_version_min'>='$min_required_min | bc -l) == 1  ]] ; then
        echo "Python version: $python_version_l"
    else
        echo -e "\e[31mPython version: $python_version_l\e[0m"
        echo -e "\e[31mPlease check your Python version >= 3.9 and make sure that the appropriate Conda env is activated.\e[0m"
        exit $1
    fi
    if [[ -d "$CONDA_PREFIX/lib/$python_lib" ]]; then
        echo "Found $python_lib within Conda environment."
    else
        echo -e "\e[31mPlease check your Python binary path and make sure that the appropriate Conda environment is activated.\e[0m"
        exit $1
    fi
}

function set_grib_definition_path {

    basedir=$PWD
    cosmo_eccodes=$CONDA_PREFIX/share/eccodes-cosmo-resources
    git clone --depth 1 --branch v2.25.0.1 https://github.com/COSMO-ORG/eccodes-cosmo-resources.git $cosmo_eccodes

    if [[ -d "$cosmo_eccodes/definitions" ]]; then
        echo 'Cosmo-eccodes-definitions were successfully retrieved.'
    else
        echo -e "\e[31mCosmo-eccodes-definitions could not be cloned.\e[0m"
        exit $1
    fi

    eccodes=$CONDA_PREFIX/share/eccodes

    if [[ -d "$eccodes/definitions" ]]; then
        echo 'Eccodes definitions were successfully retrieved.'
    else
        echo -e "\e[31mEccodes retrieval failed. \e[0m"
        exit $1
    fi

    export GRIB_DEFINITION_PATH=${cosmo_eccodes}/definitions/:${eccodes}/definitions/
    export OMPI_MCA_pml="ucx"
    export OMPI_MCA_osc="ucx"
    conda env config vars set GRIB_DEFINITION_PATH=${cosmo_eccodes}/definitions/:${eccodes}/definitions/
}


check_python
set_grib_definition_path

# ---- required for fieldextra ------

if [[ $(hostname -s) == *'tsa'* ]]; then

    echo 'Setting FIELDEXTRA_PATH for tsa'
    conda env config vars set FIELDEXTRA_PATH=/project/s83c/fieldextra/tsa/bin/fieldextra_gnu_opt_omp

elif [[ $(hostname -s) == *'daint'* ]]; then

    echo 'Setting FIELDEXTRA_PATH for daint'
    conda env config vars set FIELDEXTRA_PATH=/project/s83c/fieldextra/daint/bin/fieldextra_gnu_opt_omp

elif [[ $(hostname -s) == *'nid'* ]]; then

    echo 'Setting FIELDEXTRA_PATH for balfrin'
    conda env config vars set FIELDEXTRA_PATH=/users/oprusers/osm/bin/fieldextra
fi

# ---- required for cartopy ------

if cp env/siteconfig.py $CONDA_PREFIX/lib/$python_lib/site-packages/cartopy; then
    echo 'Cartopy configuration completed successfully.'
else
    echo -e "\e[31mEnable cartopy to modify cartopy.config by placing the env/siteconfig.py file into cartopy package source folder.\n\e[0m"\
        "\e[31mPlease make sure that you are in the parent directory of the iconarray folder while executing this setup script.\e[0m"
    exit $1
fi

echo -e "\n "\
 "Variables saved to environment: \n "\
 " "

conda env config vars list

echo -e "\n "\
    "\e[32mThe setup script completed successfully! \n \e[0m" \
    "\e[32mMake sure to deactivate your environment completely before reactivating it by running conda deactivate twice: \n \e[0m" \
    "\n "\
    "\e[32m            conda deactivate  \n \e[0m"\
    " "